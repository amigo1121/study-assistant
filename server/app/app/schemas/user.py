from pydantic import BaseModel
from datetime import datetime
from ..utils.commons import UserType


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str
    type: UserType = UserType.STUDENT
    code: str


class UserLogin(BaseModel):
    identifier: str
    password: str


class UserChangePassword(BaseModel):
    username: str
    old_password: str
    new_password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    type: UserType

    class Config:
        orm_mode = True
