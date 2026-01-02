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
            
        Note:
            If the primary model fails, it will automatically fallback in order:
            1. meta-llama/llama-3.1-405b-instruct:free
            2. alibaba/tongyi-deepresearch-30b-a3b:free
        """
        if not comments:
            return "No comments to summarize."
        
        # Model dự phòng theo thứ tự ưu tiên
        fallback_model_1 = "meta-llama/llama-3.1-405b-instruct:free"
        fallback_model_2 = "alibaba/tongyi-deepresearch-30b-a3b:free"
        
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
        
        # Thử gọi với model chính
        try:
            return self._call_model(model, prompt)
        except Exception as primary_error:
            # Nếu model chính lỗi, thử với fallback model 1
            if model != fallback_model_1:
                try:
                    print(f"Primary model '{model}' failed: {str(primary_error)}. Switching to fallback model 1 '{fallback_model_1}'")
                    return self._call_model(fallback_model_1, prompt)
                except Exception as fallback1_error:
                    # Nếu fallback 1 lỗi, thử với fallback model 2
                    try:
                        print(f"Fallback model 1 '{fallback_model_1}' failed: {str(fallback1_error)}. Switching to fallback model 2 '{fallback_model_2}'")
                        return self._call_model(fallback_model_2, prompt)
                    except Exception as fallback2_error:
                        raise Exception(f"All models failed. Primary: {str(primary_error)}, Fallback1: {str(fallback1_error)}, Fallback2: {str(fallback2_error)}")
            else:
                raise Exception(f"Failed to generate summary: {str(primary_error)}")
    
    def _call_model(self, model: str, prompt: str) -> str:
        """
        Call OpenRouter API with specific model
        
        Args:
            model: Model identifier
            prompt: Prompt to send
            
        Returns:
            Model response text
        """
        
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
        
        with httpx.Client(timeout=30.0) as client:
            response = client.post(self.BASE_URL, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if data.get("error"):
                raise Exception(data["error"].get("message"))
            return data["choices"][0]["message"]["content"]
    
    def _format_comments(self, comments: list[str]) -> str:
        """Format comments into numbered list"""
        return "\n".join([f"{i+1}. {comment}" for i, comment in enumerate(comments)])
