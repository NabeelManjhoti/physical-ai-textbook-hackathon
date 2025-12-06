from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from .content_chunk import ContentChunk


class ChatRequest(BaseModel):
    """
    Model for chat requests
    """
    query: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Model for chat responses
    """
    answer: str
    sources: List[Dict[str, Any]] = []
    session_id: str
    query: str
    timestamp: str