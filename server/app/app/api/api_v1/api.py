from fastapi import APIRouter
from .endpoints import users, security, item

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(security.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(item.router, prefix="/items")
