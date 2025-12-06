from pydantic import BaseModel
from typing import List
from enum import Enum


class IngestStatus(str, Enum):
    SUCCESS = "success"
    PROCESSING = "processing"
    ERROR = "error"


class IngestRequest(BaseModel):
    """
    Model for ingestion requests
    """
    source_path: str = "/app/docs"  # Default to the mounted docs volume in Docker
    chunk_size: int = 1000
    chunk_overlap: int = 200


class IngestResponse(BaseModel):
    """
    Model for ingestion responses
    """
    status: IngestStatus
    processed_files: int
    total_chunks: int
    errors: List[str] = []
    message: str = ""