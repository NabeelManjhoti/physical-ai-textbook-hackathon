from pydantic import BaseModel
from typing import Dict, Optional

# This is a simple in-memory storage for demonstration purposes
# In a real application, this would be replaced with a proper database

class ChapterModel(BaseModel):
    id: int
    title: str
    content: str
    order: int

# Initialize with some sample data
chapters_db: Dict[int, ChapterModel] = {
    1: ChapterModel(
        id=1,
        title="Introduction to Physical AI",
        content="# Introduction to Physical AI\n\nWelcome to the fascinating world of Physical AI...",
        order=1
    ),
    2: ChapterModel(
        id=2,
        title="Robotics Fundamentals",
        content="# Robotics Fundamentals\n\nRobots are physical agents that interact with the real world...",
        order=2
    ),
    3: ChapterModel(
        id=3,
        title="Computer Vision in Physical Systems",
        content="# Computer Vision in Physical Systems\n\nComputer vision enables robots and other physical systems to perceive their environment...",
        order=3
    )
}