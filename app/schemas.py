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
    username: str  # instead of user_id

class ProblemUpdate(BaseModel):
    name: str
    date_solved: date
    difficulty: DifficultyEnum
    topic: str
    notes: Optional[str] = None
    username: str

class ProblemOut(BaseModel):
    id: int
    name: str
    date_solved: date
    difficulty: DifficultyEnum
    topic: str
    notes: Optional[str] = None
    username: str  # add this explicitly

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True