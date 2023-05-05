from datetime import datetime
from typing import List
from pydantic import BaseModel
from .task import Task


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


class AssignmentWithTaks(Assignment):
    tasks: List[Task]
