from typing import List
from pydantic import BaseModel
from app.utils.commons import TaskStatus, Priority

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
    priority: Priority = Priority.LOW
    status: TaskStatus = TaskStatus.NOT_STARTED

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    assignment_id: int
    dependencies: List[int]
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
