from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    Text
)
from app.models.base import BaseEntity


class Accommodation(BaseEntity):
    __tablename__ = "Accommodations"

    city_id = Column("CityId", Integer, nullable=False)
    type = Column("Type", Integer, nullable=True)
    code = Column("Code", String(50), nullable=True)

    name = Column("Name", String(255), nullable=False)
    address = Column("Address", String(500), nullable=True)

    star_rating = Column("StarRating", Integer, nullable=False)
    rating = Column("Rating", Numeric(3, 2), nullable=True)
    rating_count = Column("RatingCount", Integer, nullable=True)

    description = Column("Description", Text, nullable=True)   # Rich text
    regulation = Column("Regulation", Text, nullable=True)     # Rich text

    amenities = Column("Amenities", Text, nullable=True)       # JSON (NVARCHAR(MAX))
    is_active = Column("IsActive", Boolean, default=True)

    cover_img_url = Column("CoverImgUrl", String(500), nullable=True)
    coordinates = Column("Coordinates", String(50), nullable=True)  # "lat, lon"
    
    is_deleted = Column("IsDeleted", Boolean, default=False)