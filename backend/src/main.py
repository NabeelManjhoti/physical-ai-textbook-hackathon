from fastapi import FastAPI
from src.core.config import settings
from src.api import chat, ingest


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "textbook-backend"}


@app.get("/")
async def root():
    return {"message": "Physical AI Textbook Backend API"}


# Include API routes
app.include_router(chat.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")