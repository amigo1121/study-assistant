from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas, models
from app.api.deps import get_db
from .security import get_current_user

router = APIRouter()


@router.post("/", status_code=201)
def create_assignment(
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):

    course = (
        db.query(models.Course)
        .filter(models.Course.code == assignment.course_code)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # create the new assignment
    new_assignment = models.Assignment(
        title=assignment.title,
        priority=assignment.priority,
        description=assignment.description,
        due_date=assignment.due_date,
        course_id=course.id,
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment
