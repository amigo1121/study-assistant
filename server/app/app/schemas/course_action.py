from pydantic import BaseModel


class RegisterCourse(BaseModel):
    course_code: str


class LeaveCourse(RegisterCourse):
    pass


class StudentCourseInfo(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        orm_mode = True
