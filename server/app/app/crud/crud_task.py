from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.crud import crud_course
from typing import List


def read_tasks_by_assignment_id(db: Session, assignment_id: int) -> List[schemas.Task]:
    db_tasks = (
        db.query(models.Task).filter(models.Task.assignment_id == assignment_id).all()
    )
    return [schemas.Task.from_orm(db_task) for db_task in db_tasks]


def read_tasks_by_user_id(db: Session, user_id: int) -> List[schemas.Task]:
    db_tasks = (
        db.query(models.Task)
        .join(models.Task.enrollment)
        .filter(models.Enrollment.student_id == user_id)
        .all()
    )
    return [schemas.Task.from_orm(db_task) for db_task in db_tasks]


def read_task_by_user_and_assignment(
    db: Session, user_id: int, assignment_id: int
) -> List[schemas.Task]:
    db_tasks = (
        db.query(models.Task)
        .filter(models.Task.assignment_id == assignment_id)
        .join(models.Task.enrollment)
        .filter(models.Enrollment.student_id == user_id)
        .all()
    )
    return [schemas.Task.from_orm(db_task) for db_task in db_tasks]


def create_task(db: Session, task: schemas.TaskCreate, user_id: int) -> schemas.Task:

    db_task = models.Task(
        title=task.title,
        description=task.description,
        est_hours=task.est_hours,
        enrollment_id=task.enrollment_id,
        assignment_id=task.assignment_id,
        status=task.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
