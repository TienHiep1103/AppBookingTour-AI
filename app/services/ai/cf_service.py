# app/services/cf_service.py
from sqlalchemy.orm import Session
from .cf_model import CFModel
from app.models.tour import Tour
from app.models.accommodation import Accommodation
from app.models.combo import Combo
from app.enums import ItemType
from typing import Optional

class CollaborativeFilteringService:

    @staticmethod
    def recommend(db: Session, user_id: Optional[int], item_type: int, top_n=8):
        recommended_ids = []
        
        # Nếu có user_id, thử dùng model gợi ý
        if user_id is not None:
            try:
                model = CFModel(item_type)
                recs = model.recommend(user_id, top_n)
                if recs:
                    recommended_ids = [int(r["item_id"]) for r in recs]
                    print(f"Model recommendations: {recommended_ids}")
            except Exception as e:
                print(f"CF Model error: {e}")
                recommended_ids = []
        
        # Lấy items từ DB theo item_type
        if item_type == ItemType.TOUR:
            query = db.query(Tour).filter(Tour.is_combo == False, Tour.is_active == True)
        elif item_type == ItemType.ACCOMMODATION:
            query = db.query(Accommodation).filter(Accommodation.is_active == True)
        elif item_type == ItemType.COMBO:
            query = db.query(Combo).filter(Combo.is_combo == True, Combo.is_active == True)
        else:
            return []
        
        # Nếu có gợi ý từ model, lấy các items đó trước
        result = []
        if recommended_ids:
            items = query.filter(query.column_descriptions[0]['entity'].id.in_(recommended_ids)).all()
            item_map = {i.id: i for i in items}
            result = [item_map[i] for i in recommended_ids if i in item_map]
        
        # Nếu chưa đủ top_n, bổ sung bằng các sản phẩm có rating cao
        if len(result) < top_n:
            existing_ids = [item.id for item in result]
            remaining = top_n - len(result)
            
            # Lấy các sản phẩm rating cao chưa có trong kết quả
            if existing_ids:
                fallback_items = query.filter(
                    ~query.column_descriptions[0]['entity'].id.in_(existing_ids)
                ).order_by(
                    query.column_descriptions[0]['entity'].rating.desc(),
                    query.column_descriptions[0]['entity'].rating_count.desc()
                ).limit(remaining).all()
            else:
                # Nếu không có gợi ý nào, lấy toàn bộ theo rating
                fallback_items = query.order_by(
                    query.column_descriptions[0]['entity'].rating.desc(),
                    query.column_descriptions[0]['entity'].rating_count.desc()
                ).limit(remaining).all()
            
            result.extend(fallback_items)
        
        return result[:top_n]
