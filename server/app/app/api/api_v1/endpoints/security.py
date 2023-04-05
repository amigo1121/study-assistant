from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.core.security import verify_password, hash_password
from app.api import deps
from app.crud import crud_user
from app import schemas
from jose import JWTError, jwt
from app import models

import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token")

SECRET_KEY = "3d50f0988eefe6bff4637a593e9d2ae35d4fe2386937ee450f20c67a84129ddb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str = None
    token_type: str


class TokenData(BaseModel):
    username: str


def get_user(identifier: str) -> models.User:
    db = deps.get_db().__next__()
    user_in_db = crud_user.get_user_by_username_or_email(db=db, credential=identifier)
    if user_in_db:
        return user_in_db
    else:
        return False


def authenticate_user(identifier: str, password: str):
    user = get_user(identifier=identifier)
    if not user:
        return False
    if not verify_password(password=password, hashed_password=user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(identifier=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
async def login_for_access_token(login_data: schemas.UserLogin):
    user = authenticate_user(
        identifier=login_data.identifier, password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expire)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
async def read_user_me(user: Annotated[schemas.User, Depends(get_current_user)]):
    return user


@router.post("/authorize", response_model=schemas.User)
async def authorize(token: Token):
    return get_current_user(token=token.access_token)
