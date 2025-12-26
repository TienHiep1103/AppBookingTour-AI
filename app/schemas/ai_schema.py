from pydantic import BaseModel, Field
from typing import Optional

# class AIRequest(BaseModel):
#     comment: str = Field(..., description="Bình luận cần phân loại cảm xúc", min_length=1, max_length=512)

# class AIResponse(BaseModel):
#     label: int  # 0: Negative, 1: Positive, 2: Neutral
    
# class RecommendationDetailRequest(BaseModel):
#     item_id: Optional[int]
#     item_type: Optional[int]

class GeminiSummarizeRequest(BaseModel):
    comments: list[str] = Field(..., description="List of comments to summarize", min_length=1)
    language: str = Field(default="vi", description="Language for summary (vi, en, etc.)")
    model: str = Field(default="arcee-ai/trinity-mini:free", description="OpenRouter model to use")

class GeminiSummarizeResponse(BaseModel):
    summary: str = Field(..., description="Summarized text from comments")
    total_comments: int = Field(..., description="Total number of comments processed")
    model_used: str = Field(..., description="Model used for summarization")