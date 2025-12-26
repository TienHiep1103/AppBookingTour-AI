# app/services/ai/openrouter_service.py
import httpx
from app.config import OPENROUTER_API_KEY
from typing import Optional

class OpenRouterService:
    """Service for interacting with OpenRouter API"""
    
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    def __init__(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not configured")
        self.api_key = OPENROUTER_API_KEY
    
    def summarize_comments(self, comments: list[str], language: str = "vi", model: str = "arcee-ai/trinity-mini:free") -> str:
        """
        Summarize a list of comments using OpenRouter
        
        Args:
            comments: List of comment strings to summarize
            language: Language code for the summary (vi, en, etc.)
            model: Model to use (default: arcee-ai/trinity-mini:free)
                   Popular models:
                   - arcee-ai/trinity-mini:free (Free, fast)
                   - qwen/qwen3-4b:free (Free, fast)
                   - google/gemini-2.0-flash-exp:free (Free, high quality)
                   - meta-llama/llama-3.3-70b-instruct:free (Free)
                   - openai/gpt-3.5-turbo (Paid)
        
        Returns:
            Summarized text
        """
        if not comments:
            return "No comments to summarize."
        
        # Xây dựng prompt theo ngôn ngữ
        language_prompts = {
            "vi": f"""Bạn là một trợ lý AI chuyên phân tích và tóm tắt đánh giá của khách hàng. 
Hãy tóm tắt các bình luận sau đây một cách ngắn gọn, rõ ràng và khách quan.
Hãy tập trung vào các điểm chính như: cảm nhận chung, điểm tích cực, điểm tiêu cực (nếu có).

Các bình luận ({len(comments)} bình luận):
{self._format_comments(comments)}

Hãy viết tóm tắt bằng tiếng Việt, khoảng 3-5 câu.""",
            "en": f"""You are an AI assistant specialized in analyzing and summarizing customer reviews.
Please summarize the following comments concisely, clearly and objectively.
Focus on key points such as: general sentiment, positive aspects, negative aspects (if any).

Comments ({len(comments)} comments):
{self._format_comments(comments)}

Write the summary in English, approximately 3-5 sentences."""
        }
        
        # Lấy prompt theo ngôn ngữ, mặc định tiếng Việt
        prompt = language_prompts.get(language, language_prompts["vi"])
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Tối ưu hóa cho Qwen và Arcee models - combine system và user message
        if "qwen" in model.lower() or "arcee" in model.lower():
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": f"You are a helpful assistant that summarizes customer reviews.\n\n{prompt}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        else:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes customer reviews."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(self.BASE_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def _format_comments(self, comments: list[str]) -> str:
        """Format comments into numbered list"""
        return "\n".join([f"{i+1}. {comment}" for i, comment in enumerate(comments)])
