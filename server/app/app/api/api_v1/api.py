from fastapi import APIRouter
from .endpoints import users, security, event, course, course_action

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(security.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(event.router, prefix="/events", tags=["event"])
api_router.include_router(course.router, prefix="/course", tags=["course"])
api_router.include_router(
    course_action.router, prefix="/course_action", tags=["course action"]
)
