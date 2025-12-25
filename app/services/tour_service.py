import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.models.tour import Tour


def get_all_tour(db: Session):
    return db.query(Tour).filter(Tour.is_active == True).all()