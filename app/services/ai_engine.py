from google import genai
from app.core.config import settings
from app.models.chat import ChatResponse
import time
import uuid


class GeminiService:
    
    def __init__(self):
        try:
            self.client = genai.Client(api_key=settings.google_api_key)
        except Exception as e:
            print(f"Error initializing model: {e}")
            raise e

    async def get_response(self, user_query: str) ->ChatResponse:
        start_time = time.time()

        try:

            response = await self.client.aio.models.generate_content(
                model = settings.model_name, contents=user_query)
            latency = time.time() - start_time
            usage_metadata = {
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0,
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "candidates_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0
            }
            return ChatResponse(
                response=response.text,
                sources=["Manual Gemii API"],
                usage = usage_metadata,
                request_id=str(uuid.uuid4()),
                latency_seconds=round(latency, 3)
            )
        
        except Exception as e:
            raise RuntimeError(f"Błąd Gemini API: {str(e)}")
        
ai_service = GeminiService()