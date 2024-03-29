from sqlalchemy import delete, and_
from sqlalchemy.orm import Session
from app import models, schemas
from typing import List


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_user_events(db: Session, owner_id: int, skip: int, limit: int):
    return (
        db.query(models.Event)
        .filter(models.Event.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def create_multiple_events(db: Session, events: List[schemas.EventCreate]):
    db.bulk_insert_mappings(
        models.Event,
        [
            {
                "title": event.title,
                "start": event.start,
                "end": event.end,
                "owner_id": event.owner_id,
            }
            for event in events
        ],
    )
    db.commit()
    return {"message": "Create events success"}


def update_event(db: Session, event_id: int, event: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        for field, value in event.dict(exclude_unset=True).items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event


def delete_multiple_events(db: Session, event_title: str, user_id: int):
    db.execute(
        delete(models.Event).where(
            and_(models.Event.title == event_title, models.Event.owner_id == user_id)
        )
    )
    db.commit()

    return {"message": "Remove events from calendar successfully"}
