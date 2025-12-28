from fastapi import APIRouter, Query, HTTPException

from app.db import get_db
from app.enums import ItemType
from app.schemas.combo_schema import ComboResponse
from app.schemas.ai_schema import GeminiSummarizeRequest, GeminiSummarizeResponse
from ..schemas.tour_schema import TourResponse
from ..schemas.accommodation_schema import AccommodationResponse
from ..schemas.tour_schema import TourResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.ai.recommendation_service import recommend_accommodations, recommend_tours, recommend_combos
from typing import Optional, Union
from app.services.ai.cf_service import CollaborativeFilteringService
from app.services.ai.openrouter_service import OpenRouterService

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

@router.get("/collaborative", response_model=Union[list[TourResponse], list[AccommodationResponse], list[ComboResponse]])
def recommend_collaborative(
    item_type: int = Query(..., description="1: Tour, 2: Accommodation, 3: Combo"),
    user_id: Optional[int] = Query(None, description="User ID for personalized recommendations. If null, returns top-rated items"),
    top_n: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get recommendations using Collaborative Filtering or fallback to top-rated items.
    
    - **item_type**: Type of items to recommend (1: Tour, 2: Accommodation, 3: Combo)
    - **user_id**: The user ID to get personalized recommendations. If null, returns top-rated items
    - **top_n**: Number of recommendations (default: 8, max: 20)
    
    When user_id is provided, uses CF model for personalized recommendations.
    If model returns insufficient results or user_id is null, fills with top-rated items.
    """
    return CollaborativeFilteringService.recommend(
        db=db,
        user_id=user_id,
        item_type=item_type,
        top_n=top_n
    )

@router.post("/ai/summarize", response_model=GeminiSummarizeResponse)
def summarize_comments(request: GeminiSummarizeRequest):
    try:
        openrouter_service = OpenRouterService()
        summary = openrouter_service.summarize_comments(
            comments=request.comments,
            language=request.language,
            model=request.model
        )
        
        return GeminiSummarizeResponse(
            summary=summary,
            total_comments=len(request.comments),
            model_used=request.model
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to summarize comments: {str(e)}")

@router.get("/crash-test")
async def crash():
    1 / 0