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
) -> List[schemas.TaskWithDepdend]:
    db_tasks = (
        db.query(models.Task)
        .filter(models.Task.assignment_id == assignment_id)
        .join(models.Task.enrollment)
        .filter(models.Enrollment.student_id == user_id)
        .all()
    )
    return [schemas.TaskWithDepdend.from_orm(db_task) for db_task in db_tasks]


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
        for depending_task_id in task.dependencies:
            db_dependency = models.TaskDependency(depend_on_task_id=depending_task_id)
            db_task.depends_on.append(db_dependency)
        db.add(db_task)
        db.flush()
        db.refresh(db_task)
        db.commit()
        return db_task
    except Exception as e:
        db.rollback()
        raise e


def delete_task(db: Session, task_id: int, user_id: int) -> schemas.Task:
    db_task = (
        db.query(models.Task)
        .filter_by(id=task_id)
        .join(models.Task.enrollment)
        .filter(models.Enrollment.student_id == user_id)
        .first()
    )

    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task


def update_task(
    db: Session, task_id: int, task: schemas.TaskUpdate, user_id: int
) -> schemas.Task:

    db_task = (
        db.query(models.Task)
        .filter_by(id=task_id)
        .join(models.Task.enrollment)
        .filter(models.Enrollment.student_id == user_id)
        .first()
    )

    if db_task:
        db_task.description = task.description
        db_task.title = task.title
        db_task.priority = task.priority
        db_task.status = task.status
        db_task.est_hours = task.est_hours
        db_task.depends_on = []
        for id in task.dependencies:
            db_depend = models.TaskDependency(depend_on_task_id=id)
            db_task.depends_on.append(db_depend)
        db.flush()
        db.refresh(db_task)
        db.commit()
        return db_task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
