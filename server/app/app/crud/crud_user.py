from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, update
from datetime import datetime
from app import models, schemas
from app.utils.commons import UserType
from utils.auth import hash_password


def get_user(db: Session, user_id: int):
    return (
        db.query(models.User)
        .options(joinedload(models.User.registered_courses))
        .filter(models.User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_username_or_email(db: Session, credential: str):
    return (
        db.query(models.User)
        .filter(
            or_(models.User.username == credential, models.User.email == credential)
        )
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_user_password(db: Session, user: schemas.UserChangePassword):
    new_hashed_password = hash_password(user.new_password)
    updated_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .update(
            {models.User.password_hash: new_hashed_password},
            synchronize_session="evaluate",
        )
    )
    db.commit()
    return updated_user
