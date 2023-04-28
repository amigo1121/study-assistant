from sqlalchemy.orm import Session, joinedload
from app import models, schemas
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


def get_course(db: Session, course_id: int):
    return (
        db.query(models.Course)
        .options(joinedload(models.Course.students))
        .filter(models.Course.id == course_id)
        .first()
    )


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course_schedule(
    db: Session, schedule: schemas.course.CourseScheduleBase, course_id: int
):
    db_schedule = models.CourseSchedule(course_id=course_id, **schedule.dict())

    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)


def create_course(db: Session, course: schemas.CourseCreate, teacher_id):

    db_course = models.Course(
        code=course.code,
        name=course.name,
        start_date=course.start_date,
        end_date=course.end_date,
        credits=course.credits,
        teacher_id=teacher_id,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    for schedule in course.schedules:
        create_course_schedule(db=db, schedule=schedule, course_id=db_course.id)

    return db_course


def update_course(db: Session, course_id: int, course: schemas.CourseUpdate):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course:
        for field, value in course.dict(exclude_unset=True).items():
            setattr(db_course, field, value)
        db.commit()
        db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course
