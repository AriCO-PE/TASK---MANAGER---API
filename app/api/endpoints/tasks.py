from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task, User
from app.schemas import Task as TaskSchema, TaskCreate
from app.auth import get_current_user

router = APIRouter()

@router.get("/tasks", response_model=list[TaskSchema])
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@router.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id  
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task