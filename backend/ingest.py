#!/usr/bin/env python3
"""
Standalone script to initialize the vector DB with textbook content.
This script scans the /docs directory, chunks the markdown files,
and upserts them to Qdrant.
"""

import os
import sys
from pathlib import Path
import logging
from typing import List

# Add the backend/src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.chunking_service import ChunkingService
from src.services.embedding_service import EmbeddingService
from src.services.qdrant_service import QdrantService
from src.core.config import settings
from qdrant_client.http import models

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_markdown_files(source_dir: str) -> List[tuple]:
    """
    Read all markdown files from the source directory
    Returns a list of tuples (file_path, content)
    """
    markdown_files = []
    source_path = Path(source_dir)

    if not source_path.exists():
        logger.error(f"Source directory does not exist: {source_dir}")
        return markdown_files

    for md_file in source_path.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                markdown_files.append((str(md_file), content))
                logger.info(f"Read file: {md_file}")
        except Exception as e:
            logger.error(f"Error reading file {md_file}: {e}")

    return markdown_files


def main():
    logger.info("Starting ingestion process...")

    # Initialize services
    chunking_service = ChunkingService(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
    embedding_service = EmbeddingService()
    qdrant_service = QdrantService()

    # Read markdown files
    source_dir = settings.qdrant_url.replace("http://", "").split(":")[0] if settings.qdrant_url.startswith("http://") else "/app/docs"
    # For the script, we'll use the docs directory relative to the backend
    source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    logger.info(f"Reading markdown files from: {source_dir}")

    markdown_files = read_markdown_files(source_dir)

    if not markdown_files:
        logger.warning(f"No markdown files found in {source_dir}")
        return

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

    # Print summary
    logger.info("="*50)
    logger.info("INGESTION SUMMARY")
    logger.info(f"Processed files: {processed_files}")
    logger.info(f"Total chunks created: {total_chunks}")
    logger.info(f"Total vectors upserted: {len(all_points)}")
    logger.info(f"Errors: {len(errors)}")

    if errors:
        logger.info("Errors:")
        for error in errors:
            logger.error(f"  - {error}")

    logger.info("="*50)
    logger.info("Ingestion process completed!")


if __name__ == "__main__":
    main()