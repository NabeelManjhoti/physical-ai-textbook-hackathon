from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import textbook
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API for the Physical AI Interactive Textbook",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(textbook.router, prefix="/api/v1", tags=["textbook"])

@app.get("/")
def read_root():
    return {"message": "Physical AI Textbook API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}