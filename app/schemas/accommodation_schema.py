# from pydantic import BaseModel
# from typing import Optional
# from decimal import Decimal

# class AccommodationBase(BaseModel):
#     city_id: int
#     type: Optional[int]
#     code: Optional[str]

#     name: str
#     address: Optional[str]

#     star_rating: int
#     rating: Optional[Decimal]
#     rating_count: Optional[int]

#     description: Optional[str]
#     regulation: Optional[str]
#     amenities: Optional[str]

#     is_active: bool = True
#     cover_img_url: Optional[str]
#     coordinates: Optional[str]


# class AccommodationCreate(AccommodationBase):
#     pass


# class AccommodationResponse(AccommodationBase):
#     id: int
#     num_of_rooms: Optional[int] = None
#     avg_price: Optional[Decimal] = None
#     city_name: Optional[str] = None

#     class Config:
#         from_attributes = True   # SQLAlchemy ➜ Pydantic