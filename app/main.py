from fastapi import FastAPI
import uuid
from app.models.chat import ChatRequest, ChatResponse
from app.core.config import settings
from app.services.ai_engine import ai_service

app = FastAPI(title="GenAI Agent")

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    #answer = await get_agent_response(query.message)
    response  = await ai_service.get_response(request.message)
    return response

@app.get("/info")
async def get_info():
    return {
        "project": settings.project_name,
        "model": settings.model_name,
        "debug_mode": settings.debug
    }