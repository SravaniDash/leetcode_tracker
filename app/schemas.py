from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class DifficultyEnum(str, Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"

class ProblemCreate(BaseModel):
    name: str
    date_solved: date
    difficulty: DifficultyEnum
    topic: str
    notes: Optional[str] = None

class ProblemUpdate(BaseModel):
    name: str
    date_solved: Optional[date] = None
    difficulty: Optional[DifficultyEnum] = None
    topic: Optional[str] = None
    notes: Optional[str] = None


class ProblemOut(ProblemCreate):
    id: int

    class Config:
        from_attributes = True