from .course import CourseRead, CourseWithSchedules, CourseWithAssignments
from .user import User
from pydantic import BaseModel
from typing import List, Any


class EnrollmentBase(BaseModel):
    class Config:
        orm_mode = True


class EnrollmentWithStudent(EnrollmentBase):
    student: User


class CourseWithStudent(CourseWithAssignments):
    students: List[EnrollmentWithStudent]


class EnrollmentCourse(EnrollmentBase):
    course: CourseWithAssignments


class StudentWithCourse(User):
    registered_courses: List[EnrollmentCourse]
