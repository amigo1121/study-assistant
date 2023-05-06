# these api endpoints are used for TESTING only

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_event
from app import schemas
from app import models
from datetime import date
from .security import get_current_user
from pydantic import BaseModel
import logging
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
