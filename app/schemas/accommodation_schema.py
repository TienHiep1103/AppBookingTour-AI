from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class AccommodationBase(BaseModel):
    city_id: Optional[int] = None
    type: Optional[int] = None
    code: Optional[str] = None

    name: Optional[str] = None
    address: Optional[str] = None

    star_rating: Optional[int] = None
    rating: Optional[Decimal] = None
    rating_count: Optional[int] = None

    description: Optional[str] = None
    regulation: Optional[str] = None
    amenities: Optional[str] = None

    is_active: Optional[bool] = True
    cover_img_url: Optional[str] = None
    coordinates: Optional[str] = None


class AccommodationCreate(AccommodationBase):
    pass


class AccommodationResponse(AccommodationBase):
    id: Optional[int] = None
    num_of_rooms: Optional[int] = None
    avg_price: Optional[Decimal] = None
    city_name: Optional[str] = None

    class Config:
        from_attributes = True   # SQLAlchemy ➜ Pydantic