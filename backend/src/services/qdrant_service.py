from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class QdrantService:
    """
    Service class for interacting with Qdrant vector database
    """

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Using HTTP for better compatibility
        )
        self.collection_name = settings.collection_name
        self._initialize_collection()

    def _initialize_collection(self):
        """
        Initialize the collection with appropriate vector configuration
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector size (for all-MiniLM-L6-v2: 384 dimensions)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=384,  # Default size for all-MiniLM-L6-v2 embeddings
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")
            raise

    def upsert_vectors(self, points: List[models.PointStruct]):
        """
        Upsert vectors into the collection
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Upserted {len(points)} vectors into {self.collection_name}")
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            raise

    def search_vectors(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            # Format results to include payload and score
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'text': result.payload.get('text', ''),
                    'source_file': result.payload.get('source_file', ''),
                    'source_section': result.payload.get('source_section', ''),
                    'metadata': result.payload.get('metadata', {}),
                    'score': result.score
                })

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise

    def delete_collection(self):
        """
        Delete the entire collection (useful for re-indexing)
        """
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise