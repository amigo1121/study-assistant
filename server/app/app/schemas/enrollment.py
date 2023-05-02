from .course import CourseRead
from .user import User
from pydantic import BaseModel
from typing import List


class EnrollmentBase(BaseModel):
    class Config:
        orm_mode = True


class EnrollmentWithStudent(EnrollmentBase):
    student: User


class CourseWithStudent(CourseRead):
    students: List[EnrollmentWithStudent]


class StudentWithCourse(User):
    registered_courses: List[CourseRead]
