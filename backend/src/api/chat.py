from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import uuid
from datetime import datetime
from ..models.chat import ChatRequest, ChatResponse
from ..models.content_chunk import ContentChunk
from ..services.qdrant_service import QdrantService
from ..services.embedding_service import EmbeddingService
from ..services.openai_service import OpenAIService
from ..services.search_service import SearchService
from ..core.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])


def get_services():
    """
    Dependency to get service instances
    """
    qdrant_service = QdrantService()
    embedding_service = EmbeddingService()
    openai_service = OpenAIService()
    search_service = SearchService(qdrant_service, embedding_service)
    return qdrant_service, embedding_service, openai_service, search_service


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest) -> ChatResponse:
    """
    Handle chat requests and return AI-generated responses based on textbook content
    """
    try:
        qdrant_service, embedding_service, openai_service, search_service = get_services()

        # Generate a session ID if not provided
        session_id = chat_request.session_id or str(uuid.uuid4())

        # Search for relevant content in the vector database
        relevant_content = search_service.search_content(chat_request.query)

        if not relevant_content:
            # If no relevant content is found, return a response indicating this
            return ChatResponse(
                answer="I couldn't find any relevant content in the textbook to answer your question.",
                sources=[],
                session_id=session_id,
                query=chat_request.query,
                timestamp=datetime.now().isoformat()
            )

        # Generate response using OpenAI
        answer = openai_service.generate_response(chat_request.query, relevant_content)

        # Prepare sources for the response
        sources = []
        for item in relevant_content:
            source = {
                "text": item.get("text", "")[:200] + "..." if len(item.get("text", "")) > 200 else item.get("text", ""),
                "source_file": item.get("source_file", ""),
                "source_section": item.get("source_section", ""),
                "score": item.get("score", 0.0)
            }
            sources.append(source)

        # Return the response
        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=session_id,
            query=chat_request.query,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@router.get("/health")
async def chat_health():
    """
    Health check for the chat endpoint
    """
    return {"status": "healthy", "service": "chat"}