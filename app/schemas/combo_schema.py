from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ComboBase(BaseModel):
    from_city_id: int
    to_city_id: int

    code: str
    name: str
    short_description: Optional[str]

    vehicle: int
    duration_days: int

    base_price_adult: Decimal
    base_price_children: Decimal

    amenities: Optional[str]
    description: Optional[str]
    additional_info: Optional[str]
    important_info: Optional[str]

    rating: Decimal
    rating_count: Optional[int]

    total_bookings: int
    view_count: int
    interest_count: int

    is_active: bool = True
    combo_image_cover_url: Optional[str]

class ComboResponse(ComboBase):
    id: int

    class Config:
        from_attributes = True   # SQLAlchemy ➜ Pydantic