from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_user
from app import schemas
from app.core import security
from app.utils.commons import UserType
from .security import get_current_user
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    if user.code != "" and not user.code in settings.ADMIN_CODE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Administrator code is not correct",
        )
    if user.code in settings.ADMIN_CODE:
        user.role = UserType.TEACHER
    return crud_user.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(deps.get_db)):
    db_user = crud_user.get_user_by_username_or_email(db, credential=user.identifier)
    if db_user and security.verify_password(user.password, db_user.password_hash):
        return db_user
    raise HTTPException(status_code=400, detail="Wrong username or password!")


@router.post("/changepw", response_model=int)
def change_passowrd(
    user: schemas.UserChangePassword,
    db: Session = Depends(deps.get_db),
    current_user=Depends(get_current_user),
):

    if current_user and security.verify_password(
        user.old_password, current_user.password_hash
    ):
        user.username = current_user.username
        updated_user_count = crud_user.change_user_password(db, user=user)
        return updated_user_count
    raise HTTPException(
        status_code=400, detail="User not exists or old passowrd is wrong"
    )


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.StudentWithCourse)
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
