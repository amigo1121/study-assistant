from .course import CourseRead
from .user import User
from typing import List


class CourseWithStudent(CourseRead):
    students: List[User]


class StudentWithCourse(User):
    registered_courses: List[CourseRead]
