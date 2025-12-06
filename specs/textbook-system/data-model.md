# Data Model: Physical AI & Humanoid Robotics Textbook System

**Date**: 2025-12-06
**Feature**: textbook-system
**Input**: Feature specification from `/specs/textbook-system/spec.md`

## Overview
Data models for the Physical AI & Humanoid Robotics Textbook system including content storage, user interactions, and system configuration.

## Backend Data Models

### Chat Request/Response Models
```python
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    session_id: str
```

### Content Ingestion Models
```python
class IngestRequest(BaseModel):
    source_path: str = "/docs"
    chunk_size: int = 1000
    chunk_overlap: int = 200

class IngestResponse(BaseModel):
    status: str
    processed_files: int
    total_chunks: int
    errors: List[str]
```

### Content Chunk Model (for Qdrant storage)
```python
class ContentChunk(BaseModel):
    id: str
    text: str
    source_file: str
    source_section: str
    embedding: List[float]
    metadata: Dict[str, Any]
```

## Frontend Data Models

### Chat Message Model
```typescript
interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Array<{
    title: string;
    url?: string;
  }>;
}
```

### Chat Session Model
```typescript
interface ChatSession {
  id: string;
  messages: ChatMessage[];
  createdAt: Date;
  lastActive: Date;
}
```

## Qdrant Collection Schema

### Textbook Content Collection
- **Collection Name**: `textbook_content`
- **Vector Size**: Determined by embedding model (e.g., 384 for all-MiniLM-L6-v2)
- **Distance Metric**: Cosine
- **Payload Schema**:
  ```json
  {
    "text": "string",
    "source_file": "string",
    "source_section": "string",
    "chunk_index": "integer",
    "metadata": {
      "title": "string",
      "author": "string",
      "chapter": "string",
      "section": "string"
    }
  }
  ```

## API Contract Models

### Chat Endpoint
- **Method**: POST
- **Path**: `/chat`
- **Request Body**:
  ```json
  {
    "query": "string (required)"
  }
  ```
- **Response Body**:
  ```json
  {
    "answer": "string",
    "sources": "array of objects with source information",
    "session_id": "string"
  }
  ```

### Ingest Endpoint
- **Method**: POST
- **Path**: `/ingest`
- **Request Body**:
  ```json
  {
    "source_path": "string (default: /docs)",
    "chunk_size": "integer (default: 1000)",
    "chunk_overlap": "integer (default: 200)"
  }
  ```
- **Response Body**:
  ```json
  {
    "status": "string",
    "processed_files": "integer",
    "total_chunks": "integer",
    "errors": "array of strings"
  }
  ```

## Configuration Models

### System Configuration
```python
class SystemConfig(BaseModel):
    qdrant_url: str
    qdrant_api_key: Optional[str]
    openai_api_key: str
    embedding_model: str = "all-MiniLM-L6-v2"
    collection_name: str = "textbook_content"
    chunk_size: int = 1000
    chunk_overlap: int = 200
```

### Content Processing Configuration
```python
class ProcessingConfig(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 200
    separators: List[str] = ["\n\n", "\n", " ", ""]
    embedding_batch_size: int = 32
```

## Data Flow

### Content Ingestion Flow
1. Markdown files read from `/docs` directory
2. Files parsed and split into semantic chunks
3. Chunks converted to embeddings using sentence transformer
4. Embeddings and metadata stored in Qdrant collection

### Query Processing Flow
1. User query received via POST `/chat`
2. Query converted to embedding using same model as content
3. Vector search performed in Qdrant to find relevant chunks
4. Top-k relevant chunks retrieved as context
5. OpenAI API called with query + context to generate response
6. Response returned to frontend with source information

## Validation Rules

### Content Chunk Validation
- Text length must be between 100 and 2000 characters
- Source file path must be valid
- Embedding vector must match expected dimensions

### Query Validation
- Query must not be empty
- Query length must be less than 1000 characters
- Session ID (if provided) must be valid format

### Ingestion Validation
- Source path must exist and be readable
- Chunk size must be between 100 and 5000
- Chunk overlap must be less than chunk size