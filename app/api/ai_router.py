from fastapi import APIRouter

from app.db import get_db
from app.enums import ItemType
from app.schemas.combo_schema import ComboResponse
from ..schemas.ai_schema import AIRequest, AIResponse, RecommendationDetailRequest
from ..services.ai_service import predictComment
from ..schemas.tour_schema import TourResponse
from ..schemas.accommodation_schema import AccommodationResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.ai.recommendation_service import recommend_accommodations


router = APIRouter(prefix="/api", tags=["api"])

@router.post("/predictComment", response_model=AIResponse)
def predictComment_endpoint(request: AIRequest):
    label = predictComment(request.comment)
    return AIResponse(label=label)

@router.get("/accommodations/recommendations/{item_id}", response_model=list[AccommodationResponse])
def get_recommendations(item_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    return recommend_accommodations(db, item_id, top_k=top_k)