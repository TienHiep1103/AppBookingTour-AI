from ...models.city import City
from app.services.ai.feature_store import get_city_features, build_city_features, build_tour_features, get_tour_features, build_combo_features, get_combo_features
from app.services.ai.similarity_engine import top_k_similar
from app.services.accommodation_service import get_accommodations_by_city_id, _enrich_accommodations_with_room_info
from ...models.accommodation import Accommodation
from ...models.tour import Tour
from ...models.combo import Combo
from ...schemas.accommodation_schema import AccommodationResponse
from ...schemas.tour_schema import TourResponse
from ...schemas.combo_schema import ComboResponse
from app.enums import VehicleType
import random

def recommend_accommodations(db, item_id: int, top_k: int, exclude_ids: list[int] = None):
    acc = db.query(Accommodation).get(item_id)
    if not acc or not acc.is_active:
        return []

    # Build exclude set (current accommodation + recently viewed)
    exclude_set = {item_id}
    if exclude_ids:
        exclude_set.update(exclude_ids)

    city_id = acc.city_id
    cached = get_city_features(city_id)

    if not cached:
        accommodations = get_accommodations_by_city_id(db, city_id)
        build_city_features(city_id, accommodations)
        cached = get_city_features(city_id)

    ids = cached["ids"]
    vectors = cached["vectors"]

    if item_id not in ids:
        return []

    # Get similarity scores for all accommodations in the same city
    item_index = ids.index(item_id)
    all_similar = top_k_similar(vectors, item_index, len(ids))
    
    # Filter out excluded accommodations
    similar_filtered = [(idx, score) for idx, score in all_similar if ids[idx] not in exclude_set]
    
    # Fetch all candidate accommodations from same city
    candidate_ids = [ids[idx] for idx, score in similar_filtered]
    same_city_accs = db.query(Accommodation).filter(
        Accommodation.is_active == True,
        Accommodation.id.in_(candidate_ids)
    ).all()
    
    # Create a mapping of accommodation ID to similarity score
    score_map = {ids[idx]: score for idx, score in similar_filtered}
    
    # Annotate accommodations with their similarity scores
    for accommodation in same_city_accs:
        accommodation._similarity_score = score_map.get(accommodation.id, 0)
    
    # Apply diversity re-ranking
    final_recommendations = []
    used_city_ids = set()
    used_star_ratings = set()
    used_types = set()
    
    # Phase 1: Select most diverse accommodations based on similarity and diversity
    candidates = sorted(same_city_accs, key=lambda x: x._similarity_score, reverse=True)
    
    for candidate in candidates:
        if len(final_recommendations) >= min(top_k, len(candidates)):
            break
        
        # Diversity scoring: prefer unseen combinations
        diversity_score = 0
        if candidate.city_id not in used_city_ids:
            diversity_score += 2
        if candidate.star_rating not in used_star_ratings:
            diversity_score += 1
        if candidate.type not in used_types:
            diversity_score += 1
        
        # Balance similarity and diversity
        combined_score = candidate._similarity_score * 0.7 + diversity_score * 0.3
        candidate._combined_score = combined_score
    
    # Sort by combined score and select diverse accommodations
    candidates.sort(key=lambda x: getattr(x, '_combined_score', 0), reverse=True)
    
    for candidate in candidates:
        if len(final_recommendations) >= top_k // 2:  # Fill half with similar + diverse
            break
        final_recommendations.append(candidate)
        used_city_ids.add(candidate.city_id)
        used_star_ratings.add(candidate.star_rating)
        used_types.add(candidate.type)
    
    # Phase 2: Add exploration accommodations from other cities
    if len(final_recommendations) < top_k:
        needed = top_k - len(final_recommendations)
        used_ids = {a.id for a in final_recommendations}
        used_ids.update(exclude_set)
        
        other_city_accs = db.query(Accommodation).filter(
            Accommodation.is_active == True,
            Accommodation.city_id != city_id,
            Accommodation.id.notin_(used_ids)
        ).all()
        
        if other_city_accs:
            # Prioritize different star ratings and types for exploration
            exploration_candidates = []
            for other_acc in other_city_accs:
                diversity_score = 0
                if other_acc.star_rating not in used_star_ratings:
                    diversity_score += 2
                if other_acc.type not in used_types:
                    diversity_score += 2
                if other_acc.city_id not in used_city_ids:
                    diversity_score += 1
                other_acc._exploration_score = diversity_score
                exploration_candidates.append(other_acc)
            
            # Sort by exploration score and add diverse options
            exploration_candidates.sort(key=lambda x: x._exploration_score, reverse=True)
            
            for exp_acc in exploration_candidates[:needed]:
                final_recommendations.append(exp_acc)
                used_city_ids.add(exp_acc.city_id)
                used_star_ratings.add(exp_acc.star_rating)
                used_types.add(exp_acc.type)
    
    # Phase 3: Fill remaining slots with top similar if still needed
    if len(final_recommendations) < top_k:
        needed = top_k - len(final_recommendations)
        used_ids = {a.id for a in final_recommendations}
        used_ids.update(exclude_set)
        
        remaining_candidates = [a for a in same_city_accs if a.id not in used_ids]
        remaining_candidates.sort(key=lambda x: getattr(x, '_similarity_score', 0), reverse=True)
        final_recommendations.extend(remaining_candidates[:needed])
    
    # Enrich with room info
    final_recommendations = _enrich_accommodations_with_room_info(db, final_recommendations)
    
    # Get city names
    city_ids = list(set([a.city_id for a in final_recommendations]))
    cities = db.query(City).filter(City.id.in_(city_ids)).all()
    city_map = {city.id: city.name for city in cities}
    
    # Convert to AccommodationResponse with city_name
    responses = []
    for accommodation in final_recommendations[:top_k]:  # Ensure exactly top_k
        acc_dict = AccommodationResponse.model_validate(accommodation).model_dump()
        acc_dict['city_name'] = city_map.get(accommodation.city_id)
        responses.append(AccommodationResponse(**acc_dict))
    
    return responses

def recommend_tours(db, tour_id: int, top_k: int = 5, exclude_ids: list[int] = None):
    """
    Recommend tours with diversified selection:
    - 2 most similar tours
    - 1 tour with same destination
    - 1 tour with different destination
    - 1 random tour for exploration
    """
    tour = db.query(Tour).get(tour_id)
    if not tour or not tour.is_active:
        return []
    
    # Build exclude list (current tour + recently viewed)
    exclude_set = {tour_id}
    if exclude_ids:
        exclude_set.update(exclude_ids)
    
    cached = get_tour_features()
    if not cached:
        tours = db.query(Tour).filter(Tour.is_active == True, Tour.is_combo == False).all()
        if not tours:
            return []
        build_tour_features(tours)
        cached = get_tour_features()
    
    ids = cached["ids"]
    vectors = cached["vectors"]
    
    if tour_id not in ids:
        return []
    
    # Get all active tours for re-ranking
    all_tours = db.query(Tour).filter(
        Tour.is_active == True,
        Tour.id.notin_(exclude_set),
        Tour.is_combo == False
    ).all()
    
    if not all_tours:
        return []
    
    # Group tours by destination
    same_destination = [t for t in all_tours if t.destination_city_id == tour.destination_city_id]
    different_destination = [t for t in all_tours if t.destination_city_id != tour.destination_city_id]
    
    # Get similarity scores for all tours
    index = ids.index(tour_id)
    similar = top_k_similar(vectors, index, len(ids))  # Get all similarities
    
    # Filter out excluded tours from similarity results
    similar_filtered = [(idx, score) for idx, score in similar if ids[idx] not in exclude_set]
    
    final_recommendations = []
    used_ids = set()
    
    # 1. Add most similar tours (top_k - 2 if top_k > 2, otherwise 2)
    num_similar = top_k - 2 if top_k > 2 else 2
    similar_count = 0
    for idx, score in similar_filtered:
        if similar_count >= num_similar:
            break
        tour_obj = db.query(Tour).filter(Tour.id == ids[idx], Tour.is_active == True, Tour.is_combo == False).first()
        if tour_obj:
            final_recommendations.append(tour_obj)
            used_ids.add(tour_obj.id)
            similar_count += 1
    
    # 2. Add 1 tour with same destination (not already added)
    same_dest_candidates = [t for t in same_destination if t.id not in used_ids]
    if same_dest_candidates:
        # Prefer the most similar one from same destination
        same_dest_with_score = []
        for t in same_dest_candidates:
            if t.id in ids:
                t_idx = ids.index(t.id)
                score = next((s for i, s in similar_filtered if i == t_idx), 0)
                same_dest_with_score.append((t, score))
        
        if same_dest_with_score:
            same_dest_with_score.sort(key=lambda x: x[1], reverse=True)
            selected = same_dest_with_score[0][0]
            final_recommendations.append(selected)
            used_ids.add(selected.id)
    
    # 3. Add 1 tour with different destination (not already added)
    diff_dest_candidates = [t for t in different_destination if t.id not in used_ids]
    if diff_dest_candidates:
        # Prefer the most similar one from different destination
        diff_dest_with_score = []
        for t in diff_dest_candidates:
            if t.id in ids:
                t_idx = ids.index(t.id)
                score = next((s for i, s in similar_filtered if i == t_idx), 0)
                diff_dest_with_score.append((t, score))
        
        if diff_dest_with_score:
            diff_dest_with_score.sort(key=lambda x: x[1], reverse=True)
            selected = diff_dest_with_score[0][0]
            final_recommendations.append(selected)
            used_ids.add(selected.id)
    
    # 4. Add 1 random tour for exploration (not already added)
    exploration_candidates = [t for t in all_tours if t.id not in used_ids]
    if exploration_candidates:
        random_tour = random.choice(exploration_candidates)
        final_recommendations.append(random_tour)
        used_ids.add(random_tour.id)
    
    # Trim to top_k if needed
    final_recommendations = final_recommendations[:top_k]
    
    # Get city names for departure and destination
    city_ids = set()
    for t in final_recommendations:
        city_ids.add(t.departure_city_id)
        city_ids.add(t.destination_city_id)
    
    cities = db.query(City).filter(City.id.in_(city_ids)).all()
    city_map = {city.id: city.name for city in cities}
    
    # Convert to TourResponse with city names
    responses = []
    for t in final_recommendations:
        tour_dict = TourResponse.model_validate(t).model_dump()
        tour_dict['departure_city_name'] = city_map.get(t.departure_city_id)
        tour_dict['destination_city_name'] = city_map.get(t.destination_city_id)
        responses.append(TourResponse(**tour_dict))
    
    return responses

def recommend_combos(db, combo_id: int, top_k: int = 5, exclude_ids: list[int] = None):

    combo = db.query(Combo).get(combo_id)
    if not combo or not combo.is_active:
        return []
    
    # Build exclude list (current combo + recently viewed)
    exclude_set = {combo_id}
    if exclude_ids:
        exclude_set.update(exclude_ids)
    
    cached = get_combo_features()
    if not cached:
        combos = db.query(Combo).filter(Combo.is_active == True, Combo.is_combo == True).all()
        if not combos:
            return []
        build_combo_features(combos)
        cached = get_combo_features()
    
    ids = cached["ids"]
    vectors = cached["vectors"]
    
    if combo_id not in ids:
        return []
    
    # Get all active combos for re-ranking
    all_combos = db.query(Combo).filter(
        Combo.is_active == True,
        Combo.is_combo == True,
        Combo.id.notin_(exclude_set)
    ).all()
    
    if not all_combos:
        return []
    
    # Group combos by destination and vehicle type
    same_dest_diff_vehicle = [
        c for c in all_combos 
        if c.destination_city_id == combo.destination_city_id and c.vehicle != combo.vehicle
    ]
    different_destination = [
        c for c in all_combos 
        if c.destination_city_id != combo.destination_city_id
    ]
    
    # Get similarity scores for all combos
    index = ids.index(combo_id)
    similar = top_k_similar(vectors, index, len(ids))  # Get all similarities
    
    # Filter out excluded combos from similarity results
    similar_filtered = [(idx, score) for idx, score in similar if ids[idx] not in exclude_set]
    
    final_recommendations = []
    used_ids = set()
    
    # 1. Add 2 most similar combos
    similar_count = 0
    for idx, score in similar_filtered:
        if similar_count >= 2:
            break
        combo_obj = db.query(Combo).filter(
            Combo.id == ids[idx], 
            Combo.is_active == True,
            Combo.is_combo == True
        ).first()
        if combo_obj:
            final_recommendations.append(combo_obj)
            used_ids.add(combo_obj.id)
            similar_count += 1
    
    same_dest_candidates = [c for c in same_dest_diff_vehicle if c.id not in used_ids]
    if same_dest_candidates:
        same_dest_with_score = []
        for c in same_dest_candidates:
            if c.id in ids:
                c_idx = ids.index(c.id)
                score = next((s for i, s in similar_filtered if i == c_idx), 0)
                same_dest_with_score.append((c, score))
        
        if same_dest_with_score:
            same_dest_with_score.sort(key=lambda x: x[1], reverse=True)
            selected = same_dest_with_score[0][0]
            final_recommendations.append(selected)
            used_ids.add(selected.id)
    
    diff_dest_candidates = [c for c in different_destination if c.id not in used_ids]
    if diff_dest_candidates:
        diff_dest_with_score = []
        for c in diff_dest_candidates:
            if c.id in ids:
                c_idx = ids.index(c.id)
                score = next((s for i, s in similar_filtered if i == c_idx), 0)
                diff_dest_with_score.append((c, score))
        
        if diff_dest_with_score:
            diff_dest_with_score.sort(key=lambda x: x[1], reverse=True)
            selected = diff_dest_with_score[0][0]
            final_recommendations.append(selected)
            used_ids.add(selected.id)
    
    if len(final_recommendations) < top_k:
        needed = top_k - len(final_recommendations)
        fallback_candidates = [c for c in all_combos if c.id not in used_ids]
        
        if fallback_candidates:
            # Prefer more similar ones even in fallback
            fallback_with_score = []
            for c in fallback_candidates:
                if c.id in ids:
                    c_idx = ids.index(c.id)
                    score = next((s for i, s in similar_filtered if i == c_idx), 0)
                    fallback_with_score.append((c, score))
                else:
                    fallback_with_score.append((c, 0))
            
            # Sort by score and take top ones, or random if scores are similar
            fallback_with_score.sort(key=lambda x: x[1], reverse=True)
            
            if len(fallback_with_score) > needed:
                # Mix of top similar and random
                top_half = fallback_with_score[:needed]
                for c, score in top_half:
                    final_recommendations.append(c)
                    used_ids.add(c.id)
            else:
                for c, score in fallback_with_score:
                    final_recommendations.append(c)
                    used_ids.add(c.id)
    
    final_recommendations = final_recommendations[:top_k]
    
    # Get city names
    city_ids = set()
    for c in final_recommendations:
        city_ids.add(c.departure_city_id)
        city_ids.add(c.destination_city_id)
    
    cities = db.query(City).filter(City.id.in_(city_ids)).all()
    city_map = {city.id: city.name for city in cities}
    
    # Convert to ComboResponse with city names and vehicle name
    responses = []
    for c in final_recommendations:
        combo_dict = ComboResponse.model_validate(c).model_dump()
        combo_dict['departure_city_name'] = city_map.get(c.departure_city_id)
        combo_dict['destination_city_name'] = city_map.get(c.destination_city_id)
        combo_dict['vehicle_name'] = VehicleType.get_name(c.vehicle)
        responses.append(ComboResponse(**combo_dict))
    
    return responses
