from sqlalchemy import (
    Column,
    Integer,
    Numeric
)
from app.models.base import BaseEntity


class UserFavourite(BaseEntity):
    __tablename__ = "UserFavourites"

    user_id = Column("UserId", Integer, nullable=False)
    item_id = Column("ItemId", Integer, nullable=False)
    item_type = Column("ItemType", Integer, nullable=False)  # 1: Tour, 2: Accommodation, 3: Combo
    rating = Column("Rating", Numeric(3, 2), nullable=True)
