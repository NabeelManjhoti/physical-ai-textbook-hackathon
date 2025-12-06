import re
from typing import List, Tuple
from ..models.content_chunk import ContentChunk
import hashlib
import logging

logger = logging.getLogger(__name__)


class ChunkingService:
    """
    Service for chunking content into smaller pieces for vector storage
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, source_file: str, source_section: str = "") -> List[ContentChunk]:
        """
        Split text into chunks of specified size with overlap
        """
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)
        chunk_index = 0

        while start < text_length:
            # Determine the end position
            end = start + self.chunk_size

            # If this is not the last chunk, try to break at a sentence or paragraph boundary
            if end < text_length:
                # Look for a good breaking point near the end
                search_start = end - self.chunk_overlap
                break_points = [
                    text.rfind('.', search_start, end),
                    text.rfind('!', search_start, end),
                    text.rfind('?', search_start, end),
                    text.rfind('\n\n', search_start, end),
                    text.rfind('\n', search_start, end),
                    text.rfind(' ', search_start, end)
                ]

                # Find the best breaking point (the one closest to the desired end without going over)
                valid_breaks = [bp for bp in break_points if bp != -1 and bp <= end]
                if valid_breaks:
                    end = max(valid_breaks) + 1  # Include the breaking character

            # Extract the chunk
            chunk_text = text[start:end].strip()
            if chunk_text:  # Only add non-empty chunks
                chunk_id = self._generate_chunk_id(chunk_text, source_file, chunk_index)

                chunk = ContentChunk(
                    id=chunk_id,
                    text=chunk_text,
                    source_file=source_file,
                    source_section=source_section,
                    chunk_index=chunk_index
                )
                chunks.append(chunk)

            # Move to the next chunk position
            start = end - self.chunk_overlap
            if start == end:  # In case we can't find a good breaking point
                start = end
            chunk_index += 1

        logger.info(f"Chunked {source_file} into {len(chunks)} chunks")
        return chunks

    def chunk_markdown_file(self, content: str, source_file: str) -> List[ContentChunk]:
        """
        Specialized method for chunking markdown files, preserving section context
        """
        # Split content into sections based on headers
        sections = self._split_markdown_sections(content)
        all_chunks = []

        for section_title, section_content in sections:
            chunks = self.chunk_text(section_content, source_file, section_title)
            all_chunks.extend(chunks)

        return all_chunks

    def _split_markdown_sections(self, content: str) -> List[Tuple[str, str]]:
        """
        Split markdown content into sections based on headers
        """
        # Regular expression to match markdown headers (h1, h2, h3, etc.)
        header_pattern = r'^(#{1,6})\s+(.+)$'
        lines = content.split('\n')

        sections = []
        current_section_title = "Introduction"
        current_section_content = []

        for line in lines:
            match = re.match(header_pattern, line.strip())
            if match:
                # Save the previous section if it exists
                if current_section_content:
                    sections.append((current_section_title, '\n'.join(current_section_content)))

                # Start a new section
                header_level = len(match.group(1))
                header_text = match.group(2)
                current_section_title = header_text
                current_section_content = [line]
            else:
                current_section_content.append(line)

        # Add the last section
        if current_section_content:
            sections.append((current_section_title, '\n'.join(current_section_content)))

        return sections

    def _generate_chunk_id(self, text: str, source_file: str, chunk_index: int) -> str:
        """
        Generate a unique ID for a chunk based on its content and location
        """
        content_hash = hashlib.md5((text + source_file + str(chunk_index)).encode()).hexdigest()
        return f"chunk_{content_hash[:12]}_{chunk_index}"