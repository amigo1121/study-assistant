from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_event
from app import schemas
from .security import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="Only the owner can create an event"
        )
    event.owner_id = current_user.id
    return crud_event.create_event(db=db, event=event)


@router.get("/{event_id}", response_model=schemas.Event)
def read_event(
    event_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this event"
        )
    db_event = crud_event.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if current_user.id != db_event.owner_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this event"
        )
    return db_event


@router.get("/", response_model=List[schemas.Event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db),
):
    if current_user:
        return crud_event.get_user_events(
            db, owner_id=current_user.id, skip=skip, limit=limit
        )
    raise HTTPException(status_code=403, detail="Not authorized to access this event")


@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    event: schemas.EventUpdate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db),
):

    if not current_user:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this event"
        )
    db_event = crud_event.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if current_user.id != db_event.owner_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this event"
        )
    return crud_event.update_event(db=db, event=event, event_id=event_id)


@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(
    event_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this event"
        )
    db_event = crud_event.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if current_user.id != db_event.owner_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this event"
        )
    return crud_event.delete_event(db=db, event_id=event_id)
