from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class TourBase(BaseModel):
    code: str
    name: str

    type_id: int
    category_id: int

    departure_city_id: int
    destination_city_id: int

    duration_days: int
    duration_nights: int

    max_participants: int
    min_participants: int

    base_price_adult: Decimal
    base_price_child: Decimal

    description: Optional[str]
    additional_info: Optional[str]
    important_info: Optional[str]

    rating: Decimal
    rating_count: Optional[int]

    total_bookings: int
    view_count: int
    interest_count: int

    image_main_url: Optional[str]
    is_active: bool = True

class TourResponse(TourBase):
    id: int

    class Config:
        from_attributes = True   # SQLAlchemy ➜ Pydantic