from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    """
    Walidacja inputu użytkownika
    """
    message: str = Field(
        ...,
        min_length = 2,
        max_length = 2000,
        description = "Body of user query",
        examples = ["How to setup VPN in our company"]
    )

    session_id: Optional[str] = Field(
        default = None,
        description = "Optional session id to preserve context"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description = "Metadata for AI engine",
        examples = [{"temperature": 0.7, "model_variant": "gpt-4o"}]
    )

    model_config = ConfigDict(
        str_strip_whitespace = True,  
        populate_by_name = True
    )

class ChatResponse(BaseModel):
    """
    Output modelu
    """
    response: str = Field(
        ...,
        description = "Body of AI response",
        examples = ["First you need to download OpenVPN software"]
    )

    sources: List[str] = Field(
        default = list,
        description = "Contains sources which model used",
        examples = [["Tutorial how to setup VPN", "What is VPN"]]
    )
    usage: Dict[str, int] = Field(
        default_factory=dict,
        description="Usage of tokens stats",
        examples=[{"total_tokens": 450, "prompt_tokens": 400, "completion_tokens": 50}]
    )
    request_id: str = Field(
        ..., 
        description="Unikalny identyfikator zapytania do śledzenia w logach."
    )
    
    latency_seconds: Optional[float] = Field(
        None, 
        description="Czas przetwarzania zapytania przez system."
    )

    model_config = ConfigDict(
        from_attributes=True  # Pozwala na mapowanie z obiektów ORM/innych klas
    )

class UploadResponse(BaseModel):
    filename : str
    content_type : str
    char_count : int
    status: str = "success"
    message: Optional[str] = None

