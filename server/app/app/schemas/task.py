from typing import List
from pydantic import BaseModel
from app.utils.commons import TaskStatus

# TaskDependency schema


class TaskDependencyBase(BaseModel):
    task_id: int
    depends_on_task_id: int


class TaskDependencyCreate(TaskDependencyBase):
    pass


class TaskDependency(TaskDependencyBase):
    class Config:
        orm_mode = True


# Task schema


class TaskBase(BaseModel):
    title: str
    description: str = None
    est_hours: int = None

    status: TaskStatus = TaskStatus.NOT_STARTED


class TaskCreate(TaskBase):
    enrollment_id: int
    assignment_id: int
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
