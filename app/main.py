# http://127.0.0.1:8000 --> message
# http://127.0.0.1:8000/docs --> FastAPI app

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Leetcode Tracker API is running"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/problems", response_model=schemas.ProblemOut, status_code=201)
def create_problem(
    problem: schemas.ProblemCreate,
    db: Session = Depends(get_db)
):
    existing_problem = (
        db.query(models.Problem)
        .filter(
            models.Problem.name == problem.name,
            models.Problem.date_solved == problem.date_solved,
        )
        .first()
    )

    if existing_problem:
        raise HTTPException(
            status_code=400,
            detail="Problem already logged for this date",
        )
    
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
def get_problems(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Problem)

    if difficulty:
        query = query.filter(models.Problem.difficulty == difficulty)

    if topic:
        query = query.filter(models.Problem.topic == topic)

    return query.all()

@app.get("/problems/{problem_name}", response_model=schemas.ProblemOut)
def get_problem(
    problem_name: str,
    db: Session = Depends(get_db)
):
    problem = db.query(models.Problem).filter(models.Problem.name == problem_name).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return problem

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total": db.query(models.Problem).count(),
        "easy": db.query(models.Problem).filter(models.Problem.difficulty == "Easy").count(),
        "medium": db.query(models.Problem).filter(models.Problem.difficulty == "Medium").count(),
        "hard": db.query(models.Problem).filter(models.Problem.difficulty == "Hard").count(),
    }

@app.put("/problems/{problem_name}", response_model=schemas.ProblemOut)
def update_problem(
    problem_name: str,
    updates: schemas.ProblemUpdate,
    db: Session = Depends(get_db),
):
    problem = db.query(models.Problem).filter(models.Problem.name == problem_name).first()

    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{problem_name}' not found")
    
    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(problem, field, value)

    db.commit()
    db.refresh(problem)

    return problem

@app.delete("/problems/{problem_name}")
def delete_problem(problem_name: str, db: Session = Depends(get_db)):
    problem = (
        db.query(models.Problem)
        .filter(models.Problem.name == problem_name)
        .first()
    )

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db.delete(problem)
    db.commit()

    return {"message":f"Problem '{problem_name}' deleted"}