# Physical AI & Humanoid Robotics Textbook

An interactive textbook with AI-powered assistance for learning about Physical AI and Humanoid Robotics.

## Project Structure

- `frontend/` - Docusaurus-based frontend with textbook content and chat interface
- `backend/` - FastAPI backend with RAG functionality
- `docs/` - Textbook content in markdown format

## Setup

1. Install dependencies for backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Install dependencies for frontend:
   ```bash
   cd frontend
   yarn install
   ```

3. Set up environment variables:
   ```bash
   # In the backend directory, create .env file:
   cp .env.example .env
   # Add your OpenAI API key to the .env file
   ```

4. Start the services:
   ```bash
   # Terminal 1: Start backend
   cd backend
   uvicorn src.main:app --reload

   # Terminal 2: Start frontend
   cd frontend
   yarn start
   ```