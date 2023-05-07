from datetime import date, time
from typing import List, Optional, Any
from pydantic import BaseModel
from app.utils.commons import WeekDay, EnrollmentStatus
from app import schemas
from .assignment import AssignmentWithTaks, Assignment


class CourseScheduleBase(BaseModel):
    week_day: WeekDay
    start_time: time
    end_time: time


class CourseSchedule(CourseScheduleBase):
    id: int

    class Config:
        orm_mode = True


class CourseCreate(BaseModel):
    code: str
    name: str
    start_date: date
    end_date: date
    credits: int
    schedules: List[CourseScheduleBase]


# Pydantic schema for updating a course
class CourseUpdate(BaseModel):
    code: Optional[str]
    name: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    credits: Optional[int]


class CourseRead(BaseModel):
    id: int
    code: str
    name: str
    start_date: date
    end_date: date
    credits: int
    teacher_id: int

    class Config:
        orm_mode = True


class CourseWithSchedules(CourseRead):
    schedules: List[CourseSchedule]


class CourseWithAssignments(CourseWithSchedules):
    teacher: schemas.User
    assignments: List[Assignment]
