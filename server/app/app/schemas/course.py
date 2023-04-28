from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class CourseCreate(BaseModel):
    code: str
    name: str
    start_date: date
    end_date: date
    credits: int


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

    class Config:
        orm_mode = True
