from typing import List, Dict, Any
from .qdrant_service import QdrantService
from .embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for searching content in the vector database
    """

    def __init__(self, qdrant_service: QdrantService, embedding_service: EmbeddingService):
        self.qdrant_service = qdrant_service
        self.embedding_service = embedding_service

    def search_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for content relevant to the query
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_service.generate_embedding(query)

            # Search in Qdrant
            results = self.qdrant_service.search_vectors(query_embedding, limit)

            return results
        except Exception as e:
            logger.error(f"Error searching content: {e}")
            raise

    def search_content_with_context(self, query: str, context_window: int = 1) -> List[Dict[str, Any]]:
        """
        Search for content and potentially include context from surrounding chunks
        """
        try:
            # For now, just return the basic search results
            # In the future, this could be enhanced to include surrounding context
            return self.search_content(query)
        except Exception as e:
            logger.error(f"Error searching content with context: {e}")
            raise