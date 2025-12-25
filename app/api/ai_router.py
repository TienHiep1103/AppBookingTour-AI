from fastapi import APIRouter, Query

from app.db import get_db
from app.enums import ItemType
from app.schemas.combo_schema import ComboResponse
# from ..services.ai_service import predictComment
from ..schemas.tour_schema import TourResponse
from ..schemas.accommodation_schema import AccommodationResponse
from ..schemas.tour_schema import TourResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.ai.recommendation_service import recommend_accommodations, recommend_tours, recommend_combos
from typing import Optional


router = APIRouter(prefix="/api", tags=["api"])

# @router.post("/predictComment", response_model=AIResponse)
# def predictComment_endpoint(request: AIRequest):
#     label = predictComment(request.comment)
#     return AIResponse(label=label)

@router.get("/accommodations/recommendations/{item_id}", response_model=list[AccommodationResponse])
def get_accommodation_recommendations(
    item_id: int, 
    top_k: int = 5, 
    exclude_ids: Optional[list[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get accommodation recommendations with diversity re-ranking.
    
    - **item_id**: The accommodation ID to get recommendations for
    - **top_k**: Number of recommendations (default: 5)
    - **exclude_ids**: List of accommodation IDs to exclude (e.g., recently viewed)
    """
    return recommend_accommodations(db, item_id, top_k=top_k, exclude_ids=exclude_ids)

@router.get("/tours/recommendations/{item_id}", response_model=list[TourResponse])
def get_tour_recommendations(
    item_id: int, 
    top_k: int = 5, 
    exclude_ids: Optional[list[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get tour recommendations with diversified selection.
    
    - **item_id**: The tour ID to get recommendations for
    - **top_k**: Number of recommendations (default: 5)
    - **exclude_ids**: List of tour IDs to exclude (e.g., recently viewed)
    """
    return recommend_tours(db, item_id, top_k=top_k, exclude_ids=exclude_ids)

@router.get("/combos/recommendations/{item_id}", response_model=list[ComboResponse])
def get_combo_recommendations(
    item_id: int, 
    top_k: int = 5, 
    exclude_ids: Optional[list[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get combo recommendations with diversified selection.
    
    - **item_id**: The combo ID to get recommendations for
    - **top_k**: Number of recommendations (default: 5)
    - **exclude_ids**: List of combo IDs to exclude (e.g., recently viewed)
    """
    return recommend_combos(db, item_id, top_k=top_k, exclude_ids=exclude_ids)

@router.get("/crash-test")
async def crash():
    1 / 0