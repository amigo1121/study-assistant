from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas, models
from app.api.deps import get_db
from .security import get_current_user
from app.utils.commons import UserType
from typing import List, Any

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
        name=assignment.name,
        description=assignment.description,
        due_date=assignment.due_date,
        course_id=course.id,
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


@router.put("/")
async def update_assignment(
    assignment: schemas.AssignmentUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    # Check if assignment exists
    db_assignment = (
        db.query(models.Assignment)
        .filter(models.Assignment.id == assignment.id)
        .first()
    )

    if not user or user.role != UserType.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only the teacher can create assignments"
        )

    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Update the assignment with the new data
    for field, value in assignment.dict(exclude_defaults=True).items():
        setattr(db_assignment, field, value)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):

    if not user or user.role != UserType.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only the teacher can create assignments"
        )

    assignment = (
        db.query(models.Assignment)
        .filter(models.Assignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()

    return {"message": f"Assignment with ID {assignment_id} deleted successfully"}
