from pydantic import BaseModel, Field
from typing import Optional

class AIRequest(BaseModel):
    comment: str = Field(..., description="Bình luận cần phân loại cảm xúc", min_length=1, max_length=512)

class AIResponse(BaseModel):
    label: int  # 0: Negative, 1: Positive, 2: Neutral
    
class RecommendationDetailRequest(BaseModel):
    item_id: Optional[int]
    item_type: Optional[int]