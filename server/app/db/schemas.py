from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    userIdentifier: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    credit: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

class TaskWithSubtasks(Task):
    subtasks: List['Subtask'] = []

class TaskCreateWithSubtasks(TaskCreate):
    subtasks: Optional[List['SubtaskCreate']] = []

class TaskUpdateWithSubtasks(TaskUpdate):
    subtasks: Optional[List['SubtaskUpdate']] = []

class TaskDelete(TaskBase):
    id: int

class SubtaskBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    credit: Optional[int] = None

class SubtaskCreate(SubtaskBase):
    task_id: int

class SubtaskUpdate(SubtaskBase):
    pass

class Subtask(SubtaskBase):
    id: int
    created_at: datetime
    modified_at: datetime
    task_id: int

    class Config:
        orm_mode = True

class SubtaskDelete(SubtaskBase):
    id: int