from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AsssignmentBase(BaseModel):
    name: str
    description: str
    due_date: datetime


class AssignmentCreate(AsssignmentBase):
    course_code: str
    pass


class AssignmentUpdate(AsssignmentBase):
    id: int
    pass


class Assignment(AsssignmentBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True
