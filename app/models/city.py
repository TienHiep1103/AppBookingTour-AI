from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from app.models.base import BaseEntity


class City(BaseEntity):
    __tablename__ = "Cities"

    name = Column("Name", String(255), nullable=False)
    code = Column("Code", String(50), nullable=True)
    region = Column("Region", Integer, nullable=True)
    is_popular = Column("IsPopular", Boolean, nullable=False, default=False)
    slug = Column("Slug", String(255), nullable=False)
    description = Column("Description", Text, nullable=True)
    image_url = Column("ImageUrl", String(500), nullable=True)
    is_active = Column("IsActive", Boolean, nullable=False, default=True)