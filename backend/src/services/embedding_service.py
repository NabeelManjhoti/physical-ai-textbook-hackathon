from typing import List
import logging

logger = logging.getLogger(__name__)

# Try to import the real sentence transformers, fall back to mock if not available
try:
    from sentence_transformers import SentenceTransformer
    REAL_EMBEDDING_AVAILABLE = True

    class EmbeddingService:
        """
        Service for generating embeddings using sentence transformers
        """

        def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
            self.model_name = model_name
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")

        def generate_embedding(self, text: str) -> List[float]:
            """
            Generate embedding for a single text
            """
            embedding = self.model.encode(text)
            return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)

except ImportError:
    # Use mock implementation when sentence-transformers is not available
    logger.warning("sentence-transformers not available, using mock embedding service")
    REAL_EMBEDDING_AVAILABLE = False

    class EmbeddingService:
        """
        Mock service for generating embeddings when the real sentence-transformers library is not available
        """

        def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
            self.model_name = model_name
            logger.info(f"Using mock embedding service with model: {model_name}")

        def generate_embedding(self, text: str) -> List[float]:
            """
            Generate a mock embedding for the given text
            In a real implementation, this would use sentence-transformers
            """
            import hashlib
            # Create a deterministic mock embedding based on the text content
            text_hash = hashlib.md5(text.encode()).hexdigest()
            # Convert hash to a list of floats between -1 and 1
            embedding = []
            for i in range(0, len(text_hash), 2):
                hex_pair = text_hash[i:i+2]
                val = int(hex_pair, 16) / 128.0 - 1.0  # Normalize to [-1, 1]
                embedding.append(val)
                if len(embedding) >= 10:  # Limit to 10 dimensions for mock
                    break
            # Pad with zeros if needed
            while len(embedding) < 384:  # Typical size for sentence transformers
                embedding.append(0.0)
            return embedding[:384]  # Return exactly 384 dimensions