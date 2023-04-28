from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import insert, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.course_action import RegisterCourse, LeaveCourse
from app import models

router = APIRouter()


@router.post("/register-course")
def register_course(register_course: RegisterCourse, db: Session = Depends(get_db)):
    course = (
        db.query(models.Course)
        .filter(models.Course.id == register_course.course_id)
        .first()
    )
    student = (
        db.query(models.User)
        .filter(models.User.id == register_course.student_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        stmt = insert(models.course.student_course).values(
            student_id=register_course.student_id, course_id=register_course.course_id
        )
        db.execute(stmt)
        db.commit()
        return {"message": "Course registered successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to create course registration"
        ) from e


@router.post("/leave-course")
def leave_course(leave_course: LeaveCourse, db: Session = Depends(get_db)):
    try:
        stmt = delete(models.course.student_course).where(
            models.course.student_course.c.student_id == leave_course.student_id,
            models.course.student_course.c.course_id == leave_course.course_id,
        )
        result = db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Course registration not found")
        db.commit()
        return {"message": "Course registration deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to delete course registration"
        ) from e
