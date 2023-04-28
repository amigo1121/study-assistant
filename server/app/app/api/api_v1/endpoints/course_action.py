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
        stmt = insert(models.course.student_course).values(
            student_id=student.id, course_id=course.id
        )
        db.execute(stmt)
        db.commit()
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

    course = (
        db.query(models.Course)
        .filter(models.Course.code == course_info.course_code)
        .first()
    )

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        stmt = delete(models.course.student_course).where(
            models.course.student_course.c.student_id == student.id,
            models.course.student_course.c.course_id == course.id,
        )
        result = db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Course registration not found")
        db.commit()
        return {"message": "Course deregistration deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to delete course registration"
        ) from e
