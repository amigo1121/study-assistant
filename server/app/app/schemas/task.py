from typing import List, Optional
from datetime import date, time
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    est_hours: Optional[float] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None


class TaskCreate(TaskBase):
    dependencies: Optional[List[int]] = []


class Task(TaskBase):
    id: int
    dependencies: List["Task"] = []

    class Config:
        orm_mode = True


class TaskUpdate(TaskBase):
    dependencies: Optional[List[int]] = []
