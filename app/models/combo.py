from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.models.base import BaseEntity


class Combo(BaseEntity):
    __tablename__ = "Combos"

    # ===== Basic fields =====
    from_city_id = Column("FromCityId", Integer, ForeignKey("Cities.Id"), nullable=False)
    to_city_id = Column("ToCityId", Integer, ForeignKey("Cities.Id"), nullable=False)

    code = Column("Code", String(50), nullable=False, unique=True)
    name = Column("Name", String(255), nullable=False)

    short_description = Column("ShortDescription", String(500), nullable=True)

    vehicle = Column("Vehicle", Integer, nullable=False)  # enum stored as int

    duration_days = Column("DurationDays", Integer, nullable=False)

    base_price_adult = Column("BasePriceAdult", Numeric(18, 2), nullable=False)
    base_price_children = Column("BasePriceChildren", Numeric(18, 2), nullable=False)

    amenities = Column("Amenities", Text, nullable=True)     # JSON
    description = Column("Description", Text, nullable=True)

    additional_info = Column("AdditionalInfo", Text, nullable=True)
    important_info = Column("ImportantInfo", Text, nullable=True)

    rating = Column("Rating", Numeric(3, 2), nullable=False)
    rating_count = Column("RatingCount", Integer, nullable=True)

    total_bookings = Column("TotalBookings", Integer, nullable=False)
    view_count = Column("ViewCount", Integer, nullable=False)
    interest_count = Column("InterestCount", Integer, nullable=False)

    is_active = Column("IsActive", Boolean, nullable=False, default=True)
    combo_image_cover_url = Column("ComboImageCoverUrl", String(500), nullable=True)
