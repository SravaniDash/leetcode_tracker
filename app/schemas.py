from pydantic import BaseModel
from datetime import date
from enum import Enum

class DifficultyEnum(str, Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"

class ProblemCreate(BaseModel):
    name: str
    date_solved: date
    difficulty: DifficultyEnum
    topic: str
    notes: str | None = None

class ProblemOut(ProblemCreate):
    id: int

    class Config:
        from_attributes = True