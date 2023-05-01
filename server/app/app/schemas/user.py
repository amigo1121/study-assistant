from pydantic import BaseModel
from datetime import date
from datetime import datetime
from typing import List, Optional
from ..utils.commons import UserType


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    role: UserType = UserType.STUDENT
    code: str


class UserLogin(BaseModel):
    identifier: str
    password: str


class UserChangePassword(BaseModel):
    username: str | None = None
    old_password: str
    new_password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
