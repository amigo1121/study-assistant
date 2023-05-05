from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from .security import get_current_user
from app.crud import crud_task
import logging


router = APIRouter()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


@router.get("/assignment/{assignment_id}", response_model=List[schemas.Task])
def read_tasks_by_assignment(
    assignment_id: int,
    db: Session = Depends(deps.get_db),
    # current_user: schemas.User = Depends(get_current_user),
):
    task_list = crud_task.read_tasks_by_assignment_id(
        db=db, assignment_id=assignment_id
    )
    return task_list


@router.get("/users", response_model=List[schemas.Task])
def read_tasks_by_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    task_list = crud_task.read_tasks_by_user_id(db=db, user_id=current_user.id)
    return task_list


@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    task = crud_task.create_task(db=db, task=task, user_id=current_user.id)
    return task


@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    task = crud_task.update_task(
        db=db, task_id=task_id, task=task, user_id=current_user.id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )
    return task


@router.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    task = crud_task.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )
    return task
