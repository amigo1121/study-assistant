from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def read_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def read_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    for field, value in task:
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db.query(models.Subtask).filter(models.Subtask.task_id == task_id).delete()
    db.query(models.Task).filter(models.Task.id == task_id).delete()
    db.commit()

def create_subtask(db: Session, subtask: schemas.SubtaskCreate):
    db_subtask = models.Subtask(**subtask.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

def read_subtask(db: Session, subtask_id: int):
    return db.query(models.Subtask).filter(models.Subtask.id == subtask_id).first()

def read_subtasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subtask).offset(skip).limit(limit).all()

def update_subtask(db: Session, subtask_id: int, subtask: schemas.SubtaskUpdate):
    db_subtask = db.query(models.Subtask).filter(models.Subtask.id == subtask_id).first()
    for field, value in subtask:
        setattr(db_subtask, field, value)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

def delete_subtask(db: Session, subtask_id: int):
    db.query(models.Subtask).filter(models.Subtask.id == subtask_id).delete()
    db.commit()