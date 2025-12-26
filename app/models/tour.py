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


class Tour(BaseEntity):
    __tablename__ = "Tours"

    # ===== Basic fields =====
    code = Column("Code", String(50), nullable=False, unique=True)
    name = Column("Name", String(255), nullable=False)

    type_id = Column("TypeId", Integer, ForeignKey("TourTypes.Id"), nullable=True)
    category_id = Column("CategoryId", Integer, ForeignKey("TourCategories.Id"), nullable=True)

    departure_city_id = Column("DepartureCityId", Integer, ForeignKey("Cities.Id"), nullable=False)
    destination_city_id = Column("DestinationCityId", Integer, ForeignKey("Cities.Id"), nullable=False)

    duration_days = Column("DurationDays", Integer, nullable=False)
    duration_nights = Column("DurationNights", Integer, nullable=False)

    max_participants = Column("MaxParticipants", Integer, nullable=False)
    min_participants = Column("MinParticipants", Integer, nullable=True)

    base_price_adult = Column("BasePriceAdult", Numeric(18, 2), nullable=False)
    base_price_child = Column("BasePriceChild", Numeric(18, 2), nullable=False)

    description = Column("Description", Text, nullable=True)
    additional_info = Column("AdditionalInfo", Text, nullable=True)
    important_info = Column("ImportantInfo", Text, nullable=True)

    rating = Column("Rating", Numeric(3, 2), nullable=False)
    rating_count = Column("RatingCount", Integer, nullable=True)

    total_bookings = Column("TotalBookings", Integer, nullable=False)
    view_count = Column("ViewCount", Integer, nullable=False)
    interest_count = Column("InterestCount", Integer, nullable=False)

    image_main_url = Column("ImageMainUrl", String(500), nullable=True)
    short_description = Column("ShortDescription", String(500), nullable=True)

    is_active = Column("IsActive", Boolean, nullable=False, default=True)
    is_combo = Column("IsCombo", Boolean, nullable=False, default=False)