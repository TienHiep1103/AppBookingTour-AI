from sqlalchemy.orm import Session
from app.models.combo import Combo


def get_all_combo(db: Session):
    return db.query(Combo).all()