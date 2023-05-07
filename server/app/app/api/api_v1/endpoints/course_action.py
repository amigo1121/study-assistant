from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import insert, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.api.deps import get_db
from .security import get_current_user
from app import schemas
from app.schemas.course_action import RegisterCourse, LeaveCourse
from app import models


router = APIRouter()


@router.post("/register-course")
def register_course(
    course_info: schemas.course_action.RegisterCourse,
    db: Session = Depends(get_db),
    student: schemas.User = Depends(get_current_user),
):
    course = (
        db.query(models.Course)
        .filter(models.Course.code == course_info.course_code)
        .first()
    )
    print(course_info)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        db_enrollment = models.course.Enrollment(
            student_id=student.id, course_id=course.id
        )
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return {"message": "Course registered successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to create course registration"
        ) from e


@router.post("/drop-course")
def leave_course(
    course_info: schemas.course_action.RegisterCourse,
    db: Session = Depends(get_db),
    student: schemas.User = Depends(get_current_user),
):

    db_course = (
        db.query(models.Course)
        .filter(models.Course.code == course_info.course_code)
        .first()
    )

    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        db_enrollment = (
            db.query(models.Enrollment)
            .filter_by(student_id=student.id, course_id=db_course.id)
            .first()
        )
        if not db_enrollment:
            raise HTTPException(status_code=404, detail="Course registration not found")
        db.delete(db_enrollment)
        db.flush()
        db.commit()
        return {"message": "Course deregistration deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to delete course registration"
        ) from e
