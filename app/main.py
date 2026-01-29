# http://127.0.0.1:8000 --> message
# http://127.0.0.1:8000/docs --> FastAPI app

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine) # switch to Alembic migrations
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
    # look up user by username instead of user_id
    user = db.query(models.User).filter(models.User.username == problem.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_problem = (
        db.query(models.Problem)
        .filter(
            models.Problem.name == problem.name,
            models.Problem.user_id == user.id,
        )
        .first()
    )

    if existing_problem:
        raise HTTPException(
            status_code=400,
            detail="Problem already logged for this user",
        )
    
    db_problem = models.Problem(
        name=problem.name,
        date_solved=problem.date_solved,
        difficulty=problem.difficulty,
        topic=problem.topic,
        notes=problem.notes,
        user_id=user.id
    )

    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)

    return schemas.ProblemOut(
        id=db_problem.id,
        name=db_problem.name,
        date_solved=db_problem.date_solved,
        difficulty=db_problem.difficulty,
        topic=db_problem.topic,
        notes=db_problem.notes,
        username=user.username
    )

@app.get("/problems", response_model=list[schemas.ProblemOut])
def get_problems(db: Session = Depends(get_db)):

    problems = db.query(models.Problem).all()
    return [
        schemas.ProblemOut(
            id=p.id,
            name=p.name,
            date_solved=p.date_solved,
            difficulty=p.difficulty,
            topic=p.topic,
            notes=p.notes,
            username=p.user.username
        )
        for p in problems
    ]

# TODO: Implement filtering by difficulty and/or topic
@app.get("/problems/filter", response_model=list[schemas.ProblemOut])
def filter_problems(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    '''
    Placeholder function to filter problems by difficulty, topic, or both.
    todo later
    '''
    return []

@app.get("/problems/{problem_name}", response_model=schemas.ProblemOut)
def get_problem(
    problem_name: str,
    db: Session = Depends(get_db)
):
    problem = db.query(models.Problem).filter(models.Problem.name == problem_name).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return schemas.ProblemOut(
        id=problem.id,
        name=problem.name,
        date_solved=problem.date_solved,
        difficulty=problem.difficulty,
        topic=problem.topic,
        notes=problem.notes,
        username=problem.user.username
    )

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

    user = db.query(models.User).filter(models.User.username == updates.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    problem.name = updates.name
    problem.date_solved = updates.date_solved
    problem.difficulty = updates.difficulty
    problem.topic = updates.topic
    problem.notes = updates.notes
    problem.user_id = user.id

    db.commit()
    db.refresh(problem)

    return schemas.ProblemOut(
        id=problem.id,
        name=problem.name,
        date_solved=problem.date_solved,
        difficulty=problem.difficulty,
        topic=problem.topic,
        notes=problem.notes,
        username=user.username
    )

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

@app.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{username}/problems", response_model=list[schemas.ProblemOut])
def get_user_problems(
    username: str,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    problems = db.query(models.Problem).filter(models.Problem.user_id == user.id).all()
    return [
        schemas.ProblemOut(
            id=p.id,
            name=p.name,
            date_solved=p.date_solved,
            difficulty=p.difficulty,
            topic=p.topic,
            notes=p.notes,
            username=p.user.username
        )
        for p in problems
    ]

