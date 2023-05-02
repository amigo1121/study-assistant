from .course import CourseRead, CourseWithSchedules, CourseWithAssignments
from .user import User
from pydantic import BaseModel
from typing import List


class EnrollmentBase(BaseModel):
    class Config:
        orm_mode = True


class EnrollmentWithStudent(EnrollmentBase):
    student: User


class CourseWithStudent(CourseWithAssignments):
    students: List[EnrollmentWithStudent]


class StudentWithCourse(User):
    registered_courses: List[CourseRead]
