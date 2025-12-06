// API service for chat communication

interface ChatRequest {
  query: string;
  session_id?: string;
  user_id?: string;
}

interface ChatResponse {
  answer: string;
  sources: Array<{
    text: string;
    source_file: string;
    source_section: string;
    score: number;
  }>;
  session_id: string;
  query: string;
  timestamp: string;
}

interface IngestRequest {
  source_path?: string;
  chunk_size?: number;
  chunk_overlap?: number;
}

interface IngestResponse {
  status: 'success' | 'processing' | 'error';
  processed_files: number;
  total_chunks: number;
  errors: string[];
  message: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class ChatService {
  async sendMessage(query: string, sessionId?: string): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async ingestDocuments(request: IngestRequest = {}): Promise<IngestResponse> {
    const response = await fetch(`${API_BASE_URL}/ingest/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        source_path: request.source_path || '/app/docs',
        chunk_size: request.chunk_size || 1000,
        chunk_overlap: request.chunk_overlap || 200,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${API_BASE_URL}/chat/health`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export default new ChatService();