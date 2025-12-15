from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    Time,
    Text,
    ForeignKey
)
from app.models.base import BaseEntity


class RoomType(BaseEntity):
    __tablename__ = "RoomTypes"

    accommodation_id = Column("AccommodationId", Integer, ForeignKey("Accommodations.Id"), nullable=False)
    name = Column("Name", String(255), nullable=False)
    max_adult = Column("MaxAdult", Integer, nullable=True)
    max_children = Column("MaxChildren", Integer, nullable=True)
    status = Column("Status", Boolean, nullable=True)
    price = Column("Price", Numeric(18, 2), nullable=True)
    quantity = Column("Quantity", Integer, nullable=True)
    amenities = Column("Amenities", String(500), nullable=True)  # List id: 1, 2, 3, ..
    cover_image_url = Column("CoverImageUrl", String(500), nullable=True)
    extra_adult_price = Column("ExtraAdultPrice", Numeric(18, 2), nullable=False, default=0)
    extra_children_price = Column("ExtraChildrenPrice", Numeric(18, 2), nullable=False, default=0)
    checkin_hour = Column("CheckinHour", Time, nullable=False)
    checkout_hour = Column("CheckoutHour", Time, nullable=False)
    area = Column("Area", Numeric(10, 2), nullable=False)
    view = Column("View", String(500), nullable=True)  # View biển, view đường phố ... List Id
    cancel_policy = Column("CancelPolicy", Text, nullable=True)
    vat = Column("VAT", Numeric(5, 2), nullable=True)  # Thuế VAT
    management_fee = Column("ManagementFee", Numeric(18, 2), nullable=True)  # Phụ thu quản trị
