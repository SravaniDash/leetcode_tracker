from pydantic import BaseModel
from datetime import date

class ProblemCreate(BaseModel):
    name: str
    date_solved: date
    difficulty: str
    topic: str
    notes: str | None = None

class ProblemOut(ProblemCreate):
    id: int

    class Config:
        from_attributes = True