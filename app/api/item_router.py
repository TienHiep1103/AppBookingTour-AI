# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.db import get_db
# from app.schemas.accommodation_schema import AccommodationCreate, AccommodationResponse
# from app.schemas.combo_schema import ComboResponse
# from app.schemas.tour_schema import TourResponse
# from app.services.accommodation_service import create_accommodation, get_all_accommodation, get_accommodations_by_city_id
# from app.services.combo_service import get_all_combo
# from app.services.tour_service import get_all_tour

# router = APIRouter()

# @router.post("/", response_model=AccommodationResponse)
# def create(
#     data: AccommodationCreate,
#     db: Session = Depends(get_db)
# ):
#     return create_accommodation(db, data)

# @router.get("/accommodations", response_model=list[AccommodationResponse])
# def get_all(
#     db: Session = Depends(get_db)
# ):
#     return get_accommodations_by_city_id(db, 1)

# @router.get("/tours", response_model=list[TourResponse])
# def get_all(
#     db: Session = Depends(get_db)
# ):
#     return get_all_tour(db)

# @router.get("/combos", response_model=list[ComboResponse])
# def get_all(
#     db: Session = Depends(get_db)
# ):
#     return get_all_combo(db)

