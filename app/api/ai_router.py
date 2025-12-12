from fastapi import APIRouter
from ..schemas.ai_schema import AIRequest, AIResponse
from ..services.ai_service import predictComment

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/predictComment", response_model=AIResponse)
def predictComment_endpoint(request: AIRequest):
    label = predictComment(request.comment)
    return AIResponse(label=label)
