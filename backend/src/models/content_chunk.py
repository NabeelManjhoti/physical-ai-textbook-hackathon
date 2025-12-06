from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class ContentChunk(BaseModel):
    """
    Model representing a chunk of content stored in the vector database
    """
    id: str
    text: str
    source_file: str
    source_section: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = datetime.now()
    chunk_index: Optional[int] = None