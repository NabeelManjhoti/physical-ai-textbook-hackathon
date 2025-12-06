from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.textbook import Chapter, ChapterCreate, ChapterUpdate
from app.models.textbook import chapters_db

router = APIRouter()

@router.get("/chapters", response_model=List[Chapter])
async def get_chapters():
    """Get all textbook chapters"""
    return list(chapters_db.values())

@router.get("/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter(chapter_id: int):
    """Get a specific textbook chapter by ID"""
    if chapter_id not in chapters_db:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapters_db[chapter_id]

@router.post("/chapters", response_model=Chapter)
async def create_chapter(chapter: ChapterCreate):
    """Create a new textbook chapter"""
    new_id = max(chapters_db.keys()) + 1 if chapters_db else 1
    new_chapter = Chapter(
        id=new_id,
        title=chapter.title,
        content=chapter.content,
        order=chapter.order
    )
    chapters_db[new_id] = new_chapter
    return new_chapter

@router.put("/chapters/{chapter_id}", response_model=Chapter)
async def update_chapter(chapter_id: int, chapter: ChapterUpdate):
    """Update an existing textbook chapter"""
    if chapter_id not in chapters_db:
        raise HTTPException(status_code=404, detail="Chapter not found")

    updated_chapter = chapters_db[chapter_id].copy(update=chapter.dict(exclude_unset=True))
    chapters_db[chapter_id] = updated_chapter
    return updated_chapter

@router.delete("/chapters/{chapter_id}")
async def delete_chapter(chapter_id: int):
    """Delete a textbook chapter"""
    if chapter_id not in chapters_db:
        raise HTTPException(status_code=404, detail="Chapter not found")

    del chapters_db[chapter_id]
    return {"message": "Chapter deleted successfully"}