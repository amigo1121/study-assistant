from pydantic import BaseModel


class ItemBase(BaseModel):
    content: str


class ItemCreate(ItemBase):
    owner_id: int


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
