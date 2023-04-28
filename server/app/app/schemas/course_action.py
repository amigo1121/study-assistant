from pydantic import BaseModel


class RegisterCourse(BaseModel):
    student_id: int
    course_id: int


class LeaveCourse(RegisterCourse):
    pass


class StudentCourseInfo(RegisterCourse):
    id: int

    class Config:
        orm_mode = True
