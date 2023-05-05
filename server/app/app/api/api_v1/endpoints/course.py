from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.crud import crud_course, crud_user, crud_task
from app.api import deps
from .security import get_current_user
from app.utils.commons import UserType


router = APIRouter()


@router.post("/", response_model=schemas.course.CourseWithSchedules)
def create_course(
    course: schemas.CourseCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db),
):
    if not current_user or current_user.role != UserType.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only the teacher can create a course"
        )
    try:
        return crud_course.create_course(
            db=db, course=course, teacher_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to create a course"
        )


@router.get("/registered-courses", response_model=schemas.StudentWithCourse)
def get_registered_courses(
    db: Session = Depends(deps.get_db),
    student: schemas.User = Depends(get_current_user),
):
    db_user = crud_user.get_user(db, user_id=student.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[schemas.CourseWithStudent])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses


@router.get(
    "/available-courses", response_model=List[schemas.course.CourseWithSchedules]
)
def read_available_courses(
    current_user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    if not current_user or current_user.role != UserType.STUDENT:
        raise HTTPException(status_code=403, detail="Student access only")
    courses = crud_course.get_available_courses_for_student(
        db, skip=skip, limit=limit, student_id=current_user.id
    )
    return courses


@router.get("/my-courses", response_model=List[schemas.course.CourseWithSchedules])
def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    if not current_user or current_user.role != UserType.TEACHER:
        raise HTTPException(status_code=403, detail="Only the teacher can read courses")
    courses = crud_course.get_courses_by_teacher_id(
        db, skip=skip, limit=limit, teacher_id=current_user.id
    )
    return courses


@router.get("/{course_id}", response_model=schemas.CourseWithStudent)
def read_course(course_id: int, db: Session = Depends(deps.get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.get("/code/{course_code}", response_model=schemas.enrollment.CourseWithStudent)
def get_course_by_code(
    course_code: str,
    db: Session = Depends(deps.get_db),
    current_user=Depends(get_current_user),
):
    if not current_user or current_user.role != UserType.TEACHER:
        raise HTTPException(status_code=403, detail="Only the teacher can read courses")
    db_course = crud_course.get_course_by_code(db, course_code=course_code)
    return db_course


@router.get(
    "/registered-course/{course_code}",
    response_model=schemas.course.CourseWithAssignments,
)
def get_registered_course(
    course_code: str,
    db: Session = Depends(deps.get_db),
    current_user=Depends(get_current_user),
):
    if not current_user or current_user.role != UserType.STUDENT:
        raise HTTPException(status_code=403, detail="Student access only")
    db_course = crud_course.get_course_by_code(db, course_code=course_code)
    for assignment in db_course.assignments:
        db_task = crud_task.read_task_by_user_and_assignment(
            db=db, user_id=current_user.id, assignment_id=assignment.id
        )
        assignment.tasks = db_task
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
