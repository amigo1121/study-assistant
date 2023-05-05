from fastapi import HTTPException, status
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


def get_enrollment_id(db: Session, assignment_id: int, user_id: int) -> int:
    try:
        db_assignment = db.query(models.Assignment).filter_by(id=assignment_id).first()
        db_enrollment = (
            db.query(models.Enrollment)
            .filter_by(student_id=user_id, course_id=db_assignment.course_id)
            .first()
        )
        return db_enrollment.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found"
        )


def create_task(db: Session, task: schemas.TaskCreate, user_id: int) -> schemas.Task:
    try:
        enrollment_id = get_enrollment_id(
            db, assignment_id=task.assignment_id, user_id=user_id
        )
        db_task = models.Task(
            title=task.title,
            description=task.description,
            est_hours=task.est_hours,
            assignment_id=task.assignment_id,
            status=task.status,
            priority=task.priority,
            enrollment_id=enrollment_id,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        for depending_task_id in task.dependencies:
            db_dependency = models.TaskDependency(
                task_id=db_task.id, depend_on_task_id=depending_task_id
            )
            db.add(db_dependency)
            db.commit()
            db.refresh(db_dependency)
        return db_task
    except Exception as e:
        db.rollback()
        raise e
