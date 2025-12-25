from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey
)
from app.models.tour import Tour


class Combo(Tour):
    __tablename__ = "Combos"

    id = Column("Id", Integer, ForeignKey("Tours.Id"), primary_key=True)
    
    # ===== Fields specific to Combo =====
    vehicle = Column("Vehicle", Integer, nullable=False)  # 1: Car, 2: Airplane
    is_disable_itinerary = Column("IsDisableItinerary", Boolean, nullable=False, default=False)