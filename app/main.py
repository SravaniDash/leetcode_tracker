# http://127.0.0.1:8000 --> message
# http://127.0.0.1:8000/docs --> FastAPI app

from fastapi import FastAPI, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def root():
    return {"message": "Leetcode Tracker API is running"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/problems", response_model=schemas.ProblemOut)
def create_problem(
    problem: schemas.ProblemCreate,
    db: Session = Depends(get_db)
):
    db_problem = models.Problem(
        name=problem.name,
        date_solved=problem.date_solved,
        difficulty=problem.difficulty,
        topic=problem.topic,
        notes=problem.notes,
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@app.get("/problems", response_model=list[schemas.ProblemOut])
def get_problems(db: Session = Depends(get_db)):
    return db.query(models.Problem).all()