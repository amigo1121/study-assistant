from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import logging

logging.basicConfig(
    filename="example.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)
from app.api import deps
from app import schemas
from app.crud import crud_item
from app.api.api_v1.endpoints import security
from app.sockets import sio_server


router = APIRouter()


def on_message_processed(response):
    print("response:", response)


@router.post("/", response_model=schemas.Item)
async def create_item(
    item: schemas.ItemBase,
    db: Session = Depends(deps.get_db),
    user=Depends(security.get_current_user),
):
    db_item = crud_item.create_item(
        db=db, item=schemas.ItemCreate(content=item.content, owner_id=user.id)
    )
    try:
        await sio_server.emit(
            "new_item", data={"content": db_item.content}, room=user.username
        )
        return db_item
    except Exception as e:
        logging.error(f"Exception: {e}")


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = crud_item.get_item(db=db, item_id=item_id)
    return db_item


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    item_id: int, item: schemas.ItemUpdate, db: Session = Depends(deps.get_db)
):
    db_item = crud_item.update_item(db=db, item_id=item_id, item=item)
    return db_item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(deps.get_db)):
    return crud_item.delete_item(db=db, item_id=item_id)


@router.get("/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    user=Depends(security.get_current_user),
):
    items = crud_item.get_items(db=db, skip=skip, limit=limit, owner_id=user.id)
    return items
