"""
Mock embedding service for testing purposes when sentence-transformers is not available
"""
from typing import List


class EmbeddingService:
    """
    Mock service for generating embeddings when the real sentence-transformers library is not available
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        print(f"Using mock embedding service with model: {model_name}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate a mock embedding for the given text
        In a real implementation, this would use sentence-transformers
        """
        # Return a simple mock embedding (10-dimensional vector)
        # In practice, sentence-transformers models return 384 or more dimensions
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


# For testing the mock
if __name__ == "__main__":
    service = EmbeddingService()
    result = service.generate_embedding("test sentence")
    print(f"Generated embedding: {result[:10]}... (length: {len(result)})")