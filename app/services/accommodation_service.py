from unittest import result
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.accommodation import Accommodation
from app.models.room_type import RoomType
from app.schemas.accommodation_schema import AccommodationCreate, AccommodationResponse
from typing import List

def create_accommodation(db: Session, data: AccommodationCreate):
    acc = Accommodation(**data.model_dump())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc

def get_all_accommodation(db: Session):
    return db.query(Accommodation).filter(Accommodation.is_active == True).all()

def get_accommodations_by_city_id(db: Session, city_id: int) -> List[AccommodationResponse]:
    accommodations = db.query(Accommodation).filter(Accommodation.city_id == city_id, Accommodation.is_active == True).all()
    return _enrich_accommodations_with_room_info(db, accommodations)

def get_accommodations_other_by_city_id(db: Session, city_id: int) -> List[AccommodationResponse]:
    accommodations = db.query(Accommodation).filter(Accommodation.city_id != city_id, Accommodation.is_active == True).all()
    return _enrich_accommodations_with_room_info(db, accommodations)

def _enrich_accommodations_with_room_info(db: Session, accommodations: List[Accommodation]) -> List[AccommodationResponse]:
    roomTypes = db.query(RoomType).filter(RoomType.accommodation_id.in_([acc.id for acc in accommodations])).all()
    room_info_map = {}  
    for room in roomTypes:
        acc_id = room.accommodation_id
        if acc_id not in room_info_map:
            room_info_map[acc_id] = {
                "num_of_rooms": 0,
                "total_price": 0,
                "room_count": 0
            }
        room_info_map[acc_id]["num_of_rooms"] += 1 if room.quantity else 0
        if room.price:
            room_info_map[acc_id]["total_price"] += float(room.price)
            room_info_map[acc_id]["room_count"] += 1
    result = []
    for acc in accommodations:
        acc_data = AccommodationResponse.from_orm(acc)
        room_info = room_info_map.get(acc.id, {})
        acc_data.num_of_rooms = room_info.get("num_of_rooms", 0)
        room_count = room_info.get("room_count", 0)
        if room_count > 0:
            acc_data.avg_price = round(room_info.get("total_price", 0) / room_count, 5)
        else:
            acc_data.avg_price = None
        result.append(acc_data)
    return result