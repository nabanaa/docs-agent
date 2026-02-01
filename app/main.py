from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
from app.models.chat import ChatRequest, ChatResponse, UploadResponse
from app.core.config import settings
from app.services.ai_engine import ai_service
from app.services.pdf_service import pdf_service
from app.services.rag_service import rag_service

app = FastAPI(title="GenAI Agent")

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    #answer = await get_agent_response(query.message)
    response  = await ai_service.get_response(request.message)
    return response

@app.get("/v1/info")
async def get_info():
    return {
        "project": settings.project_name,
        "model": settings.model_name,
        "debug_mode": settings.debug
    }

@app.post("/v1/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        text = await pdf_service.extract_text(content)
        rag_service.add_document(text, file.filename)
        return {
            "filename" : file.filename,
            "content_type": file.content_type,
            "char_count": len(text),
            "status": "success"
        }
    except Exception as e:
        # To zwróci dokładny opis błędu do frontendu
        import traceback
        error_details = traceback.format_exc()
        print(error_details) # Zobaczysz to w konsoli FastAPI
        raise HTTPException(status_code=500, detail=f"Błąd: {str(e)}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail = f"Error while processing {str(e)}")