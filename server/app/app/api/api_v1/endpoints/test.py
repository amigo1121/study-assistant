# these api endpoints are used for TESTING only

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_event, crud_task, crud_course
from app import schemas
from app import models
from datetime import date
from .security import get_current_user
from pydantic import BaseModel
import logging
from app.utils.toposort import topo_sort_task, construct_graph_edge
from app.utils.stats import get_task_stats
from typing import Any

router = APIRouter()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


class Event(BaseModel):
    title: str
    start: str
    end: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    events: List[Event]

    class Config:
        orm_mode = True


# class Enrollment(Base):
#     __tablename__ = "enrollments"

#     id = Column(Integer, primary_key=True)
#     student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
#     enrollment_date = Column(Date, nullable=False)
#     status = Column(Enum(EnrollmentStatus), nullable=False)

#     # relationship
#     student = relationship("User", back_populates = "registered_courses")
#     course = relationship("Course", back_populates = "students")


class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    student: User

    class Config:
        orm_mode = True


class Course(BaseModel):
    id: int
    name: str
    code: int
    start_date: date
    end_date: date
    credits: int
    teacher_id: int
    students: List[Enrollment]

    class Config:
        orm_mode = True


@router.get("/getuser", response_model=List[User])
def get_users(db: Session = Depends(deps.get_db)):
    return db.query(models.User).all()


@router.get("/courses", response_model=List[schemas.course.CourseWithAssignments])
def get_courses(db: Session = Depends(deps.get_db)):
    return db.query(models.Course).all()


@router.get(
    "/coursewithstudent", response_model=List[schemas.enrollment.CourseWithStudent]
)
def read_course(db: Session = Depends(deps.get_db)):
    return db.query(models.Course).all()


@router.get("/tasks", response_model=List[schemas.task.TaskWithDepdend])
def read_task(db: Session = Depends(deps.get_db)):
    task = db.query(models.Task).filter_by(id=11).first()

    db_dep = models.TaskDependency(task_id=11, depend_on_task_id=10)
    # db_dep=db.query(models.TaskDependency).first()
    task.depends_on = [
        models.TaskDependency(depend_on_task_id=9),
        models.TaskDependency(depend_on_task_id=11),
    ]
    db.commit()
    return db.query(models.Task).all()


@router.get("/todos", response_model=List[schemas.task.TaskWithDepdend])
def get_todos(student_id: int, db: Session = Depends(deps.get_db)):
    tasks = (
        db.query(models.Task)
        .join(models.Task.enrollment)
        .filter_by(student_id=student_id)
        .all()
    )
    return topo_sort_task(tasks)


@router.get(
    "/todos/assignment/{assignment_id}",
    response_model=List[schemas.task.TaskWithAssignmentID],
)
def get_todos_by_assignment(
    student_id: int, assignment_id: int, db: Session = Depends(deps.get_db)
):
    tasks = crud_task.read_task_by_user_and_assignment(
        db=db, user_id=student_id, assignment_id=assignment_id
    )
    return topo_sort_task(tasks)


@router.get("/remain_time/{assignment_id}")
def getremaintime(assignment_id: int, db: Session = Depends(deps.get_db)):
    return crud_course.assignment_remain_time(db=db, assignment_id=assignment_id)


@router.get(
    "/todos/assignment/edges/{assignment_id}",
    response_model=List[schemas.task.TaskGraphEdge],
)
def get_todos_edge_by_assignment(
    student_id: int, assignment_id: int, db: Session = Depends(deps.get_db)
):
    tasks = crud_task.read_task_by_user_and_assignment(
        db=db, user_id=student_id, assignment_id=assignment_id
    )
    return construct_graph_edge(tasks)


@router.get("/nodes/{assignment_id}", response_model=List[schemas.task.TaskBase])
def get_task_node_by_assignment(
    student_id: int, assignment_id: int, db: Session = Depends(deps.get_db)
):
    tasks = crud_task.read_task_by_user_and_assignment(
        db=db, user_id=student_id, assignment_id=assignment_id
    )

    return tasks


@router.get("/tasks/priority", response_model=List[int])
def task_priority(student_id: int, db: Session = Depends(deps.get_db)):
    tasks = (
        db.query(models.Task)
        .join(models.Task.enrollment)
        .filter_by(student_id=student_id)
        .all()
    )
    return get_task_stats(tasks)
