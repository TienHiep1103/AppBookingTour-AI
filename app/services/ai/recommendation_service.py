from app.models.city import City
from .feature_store import get_city_features, build_city_features, build_tour_features, get_tour_features, build_combo_features, get_combo_features
from .similarity_engine import top_k_similar
from app.services.accommodation_service import get_accommodations_by_city_id, _enrich_accommodations_with_room_info
from ...models.accommodation import Accommodation
from ...models.tour import Tour
from ...models.combo import Combo
from ...schemas.accommodation_schema import AccommodationResponse
from ...schemas.tour_schema import TourResponse
from ...schemas.combo_schema import ComboResponse
from app.enums import VehicleType
import random

def recommend_accommodations(db, item_id: int, top_k: int):
    acc = db.query(Accommodation).get(item_id)
    if not acc or not acc.is_active or acc.is_deleted:
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
            Accommodation.is_deleted == False,
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
    if not tour or not tour.is_active or tour.is_deleted:
        return []
    cached = get_tour_features()
    if not cached:
        tours = db.query(Tour).filter(Tour.is_active == True, Tour.is_deleted == False).all()
        if not tours:
            return []
        build_tour_features(tours)
        cached = get_tour_features()
    ids = cached["ids"]
    vectors = cached["vectors"]
    if tour_id not in ids:
        return []
    index = ids.index(tour_id)
    similar = top_k_similar(vectors, index, top_k)
    if not similar:
        return []
    recommended_ids = [ids[i] for i in similar]
    result = (
        db.query(Tour)
        .filter(
            Tour.is_active == True,
            Tour.is_deleted == False,
            Tour.id.in_(recommended_ids)
        )
        .all()
    )
    tour_map = {t.id: t for t in result}
    ordered = [tour_map[i] for i in recommended_ids if i in tour_map]
    
    # Get city names for departure and destination
    city_ids = set()
    for t in ordered:
        city_ids.add(t.departure_city_id)
        city_ids.add(t.destination_city_id)
    
    cities = db.query(City).filter(City.id.in_(city_ids)).all()
    city_map = {city.id: city.name for city in cities}
    
    # Convert to TourResponse with city names
    responses = []
    for t in ordered:
        tour_dict = TourResponse.model_validate(t).model_dump()
        tour_dict['departure_city_name'] = city_map.get(t.departure_city_id)
        tour_dict['destination_city_name'] = city_map.get(t.destination_city_id)
        responses.append(TourResponse(**tour_dict))
    
    return responses

def recommend_combos(db, combo_id: int, top_k: int = 5):
    combo = db.query(Combo).get(combo_id)
    if not combo or not combo.is_active or combo.is_deleted:
        return []
    print(1)
    cached = get_combo_features()
    if not cached:
        combos = db.query(Combo).filter(Combo.is_active == True, Combo.is_deleted == False).all()
        if not combos:
            return []
        print(2)     
        build_combo_features(combos)
        cached = get_combo_features()
    
    ids = cached["ids"]
    vectors = cached["vectors"]
    
    if combo_id not in ids:
        return []
    print(3)
    index = ids.index(combo_id)
    similar = top_k_similar(vectors, index, top_k)
    
    if not similar:
        return []
    print(4)
    recommended_ids = [ids[i] for i in similar]
    result = (
        db.query(Combo)
        .filter(
            Combo.is_active == True,
            Combo.is_deleted == False,
            Combo.id.in_(recommended_ids)
        )
        .all()
    )
    
    combo_map = {c.id: c for c in result}
    ordered = [combo_map[i] for i in recommended_ids if i in combo_map]
    # Get city names
    city_ids = set()
    for c in ordered:
        city_ids.add(c.departure_city_id)
        city_ids.add(c.destination_city_id)
    
    cities = db.query(City).filter(City.id.in_(city_ids)).all()
    city_map = {city.id: city.name for city in cities}
    
    # Convert to ComboResponse with city names and vehicle name
    responses = []
    for c in ordered:
        combo_dict = ComboResponse.model_validate(c).model_dump()
        combo_dict['departure_city_name'] = city_map.get(c.departure_city_id)
        combo_dict['destination_city_name'] = city_map.get(c.destination_city_id)
        combo_dict['vehicle_name'] = VehicleType.get_name(c.vehicle)
        responses.append(ComboResponse(**combo_dict))
    
    return responses
