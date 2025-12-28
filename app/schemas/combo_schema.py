from pydantic import BaseModel
from typing import Optional
from app.schemas.tour_schema import TourBase
from app.enums import VehicleType

class ComboBase(TourBase):
    vehicle: Optional[int] = None  # 1: Car, 2: Airplane
    is_disable_itinerary: Optional[bool] = False
    
class ComboResponse(ComboBase):
    id: Optional[int] = None
    vehicle_name: Optional[str] = None
    departure_city_name: Optional[str] = None
    destination_city_name: Optional[str] = None

    class Config:
        from_attributes = True   # SQLAlchemy ➜ Pydantic
        
    def __init__(self, **data):
        super().__init__(**data)
        if self.vehicle and not self.vehicle_name:
            self.vehicle_name = VehicleType.get_name(self.vehicle)