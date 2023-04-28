from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AsssignmentBase(BaseModel):
    title: str
    priority: str
    description: str
    due_date: datetime


class AssignmentCreate(AsssignmentBase):

    pass


class Assignment(AssignmentCreate):
    id: int
    course_id: int

    class Config:
        orm_mode = True
