# Quickstart Guide: Physical AI & Humanoid Robotics Textbook System

**Date**: 2025-12-06
**Feature**: textbook-system
**Input**: Feature specification from `/specs/textbook-system/spec.md`

## Overview
This guide will help you quickly set up and run the Physical AI & Humanoid Robotics Textbook system with Docusaurus frontend, FastAPI backend, and RAG functionality.

## Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+ (for frontend development)
- OpenAI API key

## Quick Setup

### 1. Clone and Prepare Repository
```bash
# Clone the repository
git clone <repository-url>
cd physical-ai-textbook

# Create environment file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Start Infrastructure
```bash
# Start Qdrant and other services
docker-compose up -d
```

### 3. Set Up Backend
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn src.main:app --reload
```

### 4. Set Up Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Ingest Textbook Content

### 1. Add Markdown Files
Place your textbook markdown files in the `frontend/docs/` directory.

### 2. Run Ingestion
```bash
# From the backend directory
python ingest.py
```

Or use the API endpoint:
```bash
curl -X POST http://localhost:8000/ingest
```

## Using the Chat Interface

1. Open your browser to `http://localhost:3000`
2. Look for the floating chat widget in the bottom-right corner
3. Click the widget to open the chat window
4. Type your question about the textbook content
5. Press Enter or click Send to get an AI-powered response

## API Endpoints

### Chat Endpoint
```
POST /chat
Content-Type: application/json

{
  "query": "Your question about the textbook content"
}
```

### Ingest Endpoint
```
POST /ingest
Content-Type: application/json

{
  "source_path": "/docs",
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

## Development Commands

### Backend Development
```bash
# Run backend with auto-reload
uvicorn src.main:app --reload

# Run tests
pytest

# Format code
black src/
```

### Frontend Development
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Infrastructure
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Check if services are already running: `docker-compose ps`
   - Kill existing processes or use different ports

2. **API key errors**
   - Verify OpenAI API key is set in `.env` file
   - Check for typos in the API key

3. **Qdrant connection errors**
   - Ensure Qdrant service is running: `docker-compose logs qdrant`
   - Check connection URL in configuration

4. **Content not appearing in chat**
   - Verify ingestion completed successfully
   - Check that markdown files are in the correct directory
   - Confirm Qdrant collection has content

### Environment Variables
Make sure these variables are set in your `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_if_set
```

## Next Steps

1. Customize the chat widget styling in `frontend/src/components/ChatWidget.tsx`
2. Add more textbook content to the `frontend/docs/` directory
3. Configure additional settings in `backend/src/config.py`
4. Set up production deployment using GitHub Pages for frontend and container hosting for backend