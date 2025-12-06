from pydantic import BaseModel
from typing import Optional

class ChapterBase(BaseModel):
    title: str
    content: str
    order: int

class ChapterCreate(ChapterBase):
    pass

class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None

class Chapter(ChapterBase):
    id: int

    class Config:
        from_attributes = True