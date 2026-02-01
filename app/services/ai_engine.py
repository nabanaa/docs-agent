from google import genai
from app.core.config import settings
from app.models.chat import ChatResponse
from app.services.rag_service import rag_service
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
            results = rag_service.query_with_metadata(user_query, n_results=3)
            
            context_chunks = results.get("documents", [])
            metadatas = results.get("metadatas", [])
            potential_sources = list(set([m.get("source") for m in metadatas])) if metadatas else []
            context_text = "\n---\n".join(context_chunks) if context_chunks else ""
            prompt = f"""
            Jesteś inteligentnym asystentem. Twoim zadaniem jest odpowiadanie na pytania użytkownika w oparciu o dostarczony KONTEKST, który pochodzi z prywatnych dokumentów.

            ZASADY ODPOWIADANIA:
            1. Jeśli odpowiedź znajduje się w KONTEKŚCIE, odpowiedz na podstawie tych danych i wspomnij, że informacje pochodzą z dokumentów.
            2. Jeśli pytania NIE DA SIĘ odpowiedzieć na podstawie KONTEKSTU, ale jest to pytanie dotyczące wiedzy ogólnej (np. historia, nauka, fakty powszechnie znane), odpowiedz używając swojej wiedzy ogólnej, zaznaczając jednak, że tych informacji nie ma w Twoich dokumentach.
            3. Jeśli pytanie jest specyficzne dla Twoich dokumentów (np. o konkretną umowę, datę spotkania), a odpowiedzi nie ma w KONTEKŚCIE – napisz uczciwie "Nie znalazłem takich informacji w udostępnionych dokumentach".
            4. Nigdy nie zmyślaj faktów dotyczących prywatnych danych.

            KONTEKST:
            {context_text}
            
            PYTANIE:
            {user_query}
            """

            response = await self.client.aio.models.generate_content(
                model = settings.model_name, contents=prompt)
            low_conf_phrases = [
                "nie znalazłem takich informacji w udostępnionych dokumentach",
                "mojej wiedzy ogólnej",
                "tych informacji nie ma w Twoich dokumentach",
                "nie ma w udostępnionym kontekście"
            ]
            
            is_general_knowledge = any(phrase in response.text.lower() for phrase in low_conf_phrases)

            if is_general_knowledge or not context_chunks:
                sources = ["General Knowledge"]
            else:
                sources = potential_sources
            latency = time.time() - start_time
            usage_metadata = {
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0,
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "candidates_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0
            }
            return ChatResponse(
                response=response.text,
                sources= sources,
                usage = usage_metadata,
                request_id=str(uuid.uuid4()),
                latency_seconds=round(latency, 3)
            )
        
        except Exception as e:
            raise RuntimeError(f"Błąd Gemini API: {str(e)}")
        
ai_service = GeminiService()