from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import os
import logging
from pathlib import Path

from ..models.ingest import IngestRequest, IngestResponse, IngestStatus
from ..services.chunking_service import ChunkingService
from ..services.embedding_service import EmbeddingService
from ..services.qdrant_service import QdrantService
from ..core.config import settings

router = APIRouter(prefix="/ingest", tags=["ingest"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=IngestResponse)
async def ingest_endpoint(ingest_request: IngestRequest) -> IngestResponse:
    """
    Ingest markdown files from the specified source path into the vector database
    """
    try:
        # Initialize services
        chunking_service = ChunkingService(
            chunk_size=ingest_request.chunk_size,
            chunk_overlap=ingest_request.chunk_overlap
        )
        embedding_service = EmbeddingService()
        qdrant_service = QdrantService()

        # Validate source path
        source_path = Path(ingest_request.source_path)
        if not source_path.exists():
            raise HTTPException(status_code=400, detail=f"Source path does not exist: {ingest_request.source_path}")

        if not source_path.is_dir():
            raise HTTPException(status_code=400, detail=f"Source path is not a directory: {ingest_request.source_path}")

        # Read markdown files
        markdown_files = []
        for md_file in source_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    markdown_files.append((str(md_file), content))
                    logger.info(f"Read file: {md_file}")
            except Exception as e:
                logger.error(f"Error reading file {md_file}: {e}")

        if not markdown_files:
            return IngestResponse(
                status=IngestStatus.SUCCESS,
                processed_files=0,
                total_chunks=0,
                errors=[f"No markdown files found in {ingest_request.source_path}"],
                message="No markdown files to process"
            )

        # Process each file
        all_points = []
        processed_files = 0
        total_chunks = 0
        errors = []

        for file_path, content in markdown_files:
            try:
                logger.info(f"Processing file: {file_path}")

                # Chunk the content
                chunks = chunking_service.chunk_markdown_file(content, file_path)
                logger.info(f"Created {len(chunks)} chunks for {file_path}")

                # Generate embeddings for all chunks
                texts = [chunk.text for chunk in chunks]
                embeddings = embedding_service.generate_embeddings(texts)

                # Create Qdrant points
                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    from qdrant_client.http import models
                    point = models.PointStruct(
                        id=chunk.id,
                        vector=embedding,
                        payload={
                            "text": chunk.text,
                            "source_file": chunk.source_file,
                            "source_section": chunk.source_section,
                            "metadata": {
                                "chunk_index": chunk.chunk_index,
                                "created_at": chunk.created_at.isoformat()
                            }
                        }
                    )
                    all_points.append(point)

                processed_files += 1
                total_chunks += len(chunks)
            except Exception as e:
                error_msg = f"Error processing file {file_path}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Upsert all points to Qdrant
        if all_points:
            logger.info(f"Upserting {len(all_points)} vectors to Qdrant...")
            try:
                qdrant_service.upsert_vectors(all_points)
                logger.info("Successfully upserted vectors to Qdrant")
            except Exception as e:
                error_msg = f"Error upserting vectors to Qdrant: {e}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Prepare response
        if errors:
            status = IngestStatus.ERROR if processed_files == 0 else IngestStatus.SUCCESS
            message = f"Processing completed with {len(errors)} errors. See errors list for details."
        else:
            status = IngestStatus.SUCCESS
            message = f"Successfully processed {processed_files} files and created {total_chunks} chunks."

        return IngestResponse(
            status=status,
            processed_files=processed_files,
            total_chunks=total_chunks,
            errors=errors,
            message=message
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing ingest request: {str(e)}")


@router.get("/health")
async def ingest_health():
    """
    Health check for the ingest endpoint
    """
    return {"status": "healthy", "service": "ingest"}