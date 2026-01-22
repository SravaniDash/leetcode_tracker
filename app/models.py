from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_solved = Column(Date)
    difficulty = Column(String)
    topic = Column(String)
    notes = Column(String)

    