from fastapi import APIRouter
from .endpoints import (
    users,
    security,
    event,
    course,
    course_action,
    assignment,
    test,
    task,
)

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(security.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(event.router, prefix="/events", tags=["event"])
api_router.include_router(course.router, prefix="/course", tags=["course"])
api_router.include_router(
    course_action.router, prefix="/course-action", tags=["course action"]
)
api_router.include_router(assignment.router, prefix="/assignments", tags=["assignment"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
