from pydantic import BaseModel
from datetime import datetime

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
    created_at: datetime

    class Config:
        orm_mode = True