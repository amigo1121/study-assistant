from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.crud import crud_course
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.user.CourseRead)
def create_course(course: schemas.CourseCreate, db: Session = Depends(deps.get_db)):
    return crud_course.create_course(db=db, course=course)


@router.get("/", response_model=List[schemas.CourseWithStudent])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses


@router.get("/{course_id}", response_model=schemas.CourseWithStudent)
def read_course(course_id: int, db: Session = Depends(deps.get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.put("/{course_id}", response_model=schemas.CourseRead)
def update_course(
    course_id: int, course: schemas.CourseUpdate, db: Session = Depends(deps.get_db)
):
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud_course.update_course(db=db, course_id=course_id, course=course)


@router.delete("/{course_id}", response_model=schemas.CourseRead)
def delete_course(course_id: int, db: Session = Depends(deps.get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud_course.delete_course(db=db, course_id=course_id)
