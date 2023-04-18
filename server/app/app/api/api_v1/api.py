from fastapi import APIRouter
from .endpoints import users, security

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(security.router, prefix="/oauth", tags=["oauth"])
