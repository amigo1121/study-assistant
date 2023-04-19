from fastapi import APIRouter
from .endpoints import users, security, event

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(security.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(event.router, prefix="/events", tags=["event"])
