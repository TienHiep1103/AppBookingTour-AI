from app.models.city import City
from .feature_store import get_city_features, build_city_features
from .similarity_engine import top_k_similar
from app.services.accommodation_service import get_accommodations_by_city_id, _enrich_accommodations_with_room_info
from ...models.accommodation import Accommodation
from ...schemas.accommodation_schema import AccommodationResponse
import random
from .cache import get_features

def recommend_accommodations(db, item_id: int, top_k: int):
    acc = db.query(Accommodation).get(item_id)
    if not acc:
        return []

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

    item_index = ids.index(item_id)
    indices = top_k_similar(vectors, item_index, top_k)

    # Select accommodations based on indices
    recommended_ids = [ids[i] for i in indices]
    result = db.query(Accommodation).filter(Accommodation.is_active == True, Accommodation.id.in_(recommended_ids)).all()
    result = _enrich_accommodations_with_room_info(db, result)
    
    # If not enough results, add random accommodations from other cities
    if len(result) < top_k:
        needed = top_k - len(result)
        other_accs = db.query(Accommodation).filter(
            Accommodation.is_active == True,
            Accommodation.city_id != city_id,
            Accommodation.id.notin_(recommended_ids)
        ).all()
        
        if other_accs:
            additional = random.sample(other_accs, min(needed, len(other_accs)))
            additional = _enrich_accommodations_with_room_info(db, additional)
            result.extend(additional)
    
    # Get city name for each accommodation
    city_ids = list(set([acc.city_id for acc in result]))
    cities = db.query(City).filter(City.id.in_(city_ids)).all()
    city_map = {city.id: city.name for city in cities}
    
    # Convert to AccommodationResponse with city_name
    responses = []
    for acc in result:
        acc_dict = AccommodationResponse.model_validate(acc).model_dump()
        acc_dict['city_name'] = city_map.get(acc.city_id)
        responses.append(AccommodationResponse(**acc_dict))
    
    return responses

def recommend_tours(db, tour_id: int, top_k: int = 5):
    tour = db.query(Tour).get(tour_id)
    if not tour or not tour.is_active:
        return []
    cached = get_features("tour")
    if not cached:
        tours = db.query(Tour).filter(Tour.is_active == True).all()
        if not tours:
            return []

        build_tour_features(tours)
        cached = get_features("tour")
    ids = cached["ids"]
    vectors = cached["vectors"]
    if tour_id not in ids:
        return []
    index = ids.index(tour_id)
    similar = top_k_similar(vectors, index, top_k)
    if not similar:
        return []
    recommended_ids = [ids[i] for i, _ in similar]
    result = (
        db.query(Tour)
        .filter(
            Tour.is_active == True,
            Tour.id.in_(recommended_ids)
        )
        .all()
    )
    tour_map = {t.id: t for t in result}
    ordered = [tour_map[i] for i in recommended_ids if i in tour_map]
    return [
        {
            "tour_id": t.id,
            "name": t.name,
            "score": score
        }
        for t, (_, score) in zip(ordered, similar)
    ]
