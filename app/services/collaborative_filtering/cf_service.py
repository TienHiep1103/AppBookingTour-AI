import numpy as np
from sqlalchemy.orm import Session
from typing import Union, List
from .cf_model import (
    USER_FACTORS,
    ITEM_FACTORS,
    USER_ID_TO_INDEX,
    ITEM_ID_TO_INDEX,
    INDEX_TO_ITEM_ID
)
from app.models.tour import Tour
from app.models.accommodation import Accommodation
from app.models.combo import Combo
from app.enums import ItemType


class CollaborativeFilteringService:
    """
    Collaborative Filtering using Matrix Factorization
    """

    @staticmethod
    def predict_rating(user_id: int, item_id: int):
        if user_id not in USER_ID_TO_INDEX or item_id not in ITEM_ID_TO_INDEX:
            return None

        u_idx = USER_ID_TO_INDEX[user_id]
        i_idx = ITEM_ID_TO_INDEX[item_id]

        return float(np.dot(USER_FACTORS[u_idx], ITEM_FACTORS[i_idx]))

    @staticmethod
    def recommend_items(user_id: int, top_n: int = 5):
        if user_id not in USER_ID_TO_INDEX:
            return []

        u_idx = USER_ID_TO_INDEX[user_id]
        scores = USER_FACTORS[u_idx] @ ITEM_FACTORS.T

        top_indices = scores.argsort()[::-1][:top_n]

        return [
            {
                "item_id": int(INDEX_TO_ITEM_ID[int(i)].item() if hasattr(INDEX_TO_ITEM_ID[int(i)], 'item') else INDEX_TO_ITEM_ID[int(i)]),
                "score": float(scores[i])
            }
            for i in top_indices
        ]

    @staticmethod
    def get_recommendations_by_type(
        db: Session,
        user_id: int,
        item_type: int,
        top_n: int = 5
    ) -> Union[List[Tour], List[Accommodation], List[Combo]]:
        """
        Get personalized recommendations for a specific item type.
        
        Args:
            db: Database session
            user_id: User ID to get recommendations for
            item_type: Type of items (1: Tour, 2: Accommodation, 3: Combo)
            top_n: Number of recommendations
            
        Returns:
            List of Tour, Accommodation, or Combo objects
        """
        # Get item IDs from collaborative filtering
        recommendations = CollaborativeFilteringService.recommend_items(user_id=user_id, top_n=top_n)
        
        if not recommendations:
            return []
        
        # Extract item IDs and ensure they are native Python ints
        item_ids = [int(rec["item_id"]) for rec in recommendations]
        
        # Query database based on item_type
        if item_type == ItemType.TOUR:
            items = db.query(Tour).filter(Tour.id.in_(item_ids)).all()
        elif item_type == ItemType.ACCOMMODATION:
            items = db.query(Accommodation).filter(Accommodation.id.in_(item_ids)).all()
        elif item_type == ItemType.COMBO:
            items = db.query(Combo).filter(Combo.id.in_(item_ids)).all()
        else:
            return []
        
        # Sort by recommendation order
        id_to_item = {item.id: item for item in items}
        return [id_to_item[item_id] for item_id in item_ids if item_id in id_to_item]
