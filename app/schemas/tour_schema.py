from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class TourBase(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    type_id: Optional[int] = None
    category_id: Optional[int] = None

    departure_city_id: Optional[int] = None
    destination_city_id: Optional[int] = None

    duration_days: Optional[int] = None
    duration_nights: Optional[int] = None

    max_participants: Optional[int] = None
    min_participants: Optional[int] = None

    base_price_adult: Optional[Decimal] = None
    base_price_child: Optional[Decimal] = None

    description: Optional[str] = None
    additional_info: Optional[str] = None
    important_info: Optional[str] = None

    rating: Optional[Decimal] = None
    rating_count: Optional[int] = None

    total_bookings: Optional[int] = None
    view_count: Optional[int] = None
    interest_count: Optional[int] = None

    image_main_url: Optional[str] = None
    short_description: Optional[str] = None
    is_active: Optional[bool] = True

class TourResponse(TourBase):
    id: Optional[int] = None
    departure_city_name: Optional[str] = None
    destination_city_name: Optional[str] = None

    class Config:
        from_attributes = True   # SQLAlchemy ➜ Pydantic