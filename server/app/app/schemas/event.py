from typing import Optional
from pydantic import BaseModel
from typing import List


class EventBase(BaseModel):
    title: str
    start: str
    end: str


class EventCreate(EventBase):
    owner_id: int | None = None


class MultilpleEventCreate(BaseModel):
    events: List[EventCreate]

    class Config:
        orm_mode = True


class Event(EventBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class EventUpdate(EventBase):
    title: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


class EventDelete(BaseModel):
    id: int
