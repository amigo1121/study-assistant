from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Table,
    UniqueConstraint,
    Time,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from app.utils.commons import EnrollmentStatus, WeekDay, TaskStatus
from app.db.base_class import Base
from datetime import date


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False, default=date.today())
    status = Column(
        Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.ACTIVE
    )

    # relationship
    student = relationship("User", back_populates="registered_courses")
    course = relationship("Course", back_populates="students")


class CourseSchedule(Base):
    __tablename__ = "course_schedule"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    week_day = Column(Enum(WeekDay), nullable=False)

    # relationship
    course = relationship("Course", back_populates="schedules")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    credits = Column(Integer, nullable=False)
    teacher_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # relationship
    students = relationship("Enrollment", back_populates="course")
    teacher = relationship("User", back_populates="teaching_courses")
    assignments = relationship("Assignment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )

    # relationship
    course = relationship("Course", back_populates="assignments")


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    est_hours = Column(Integer)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)

    # relationships

    # depends_on = relationship("TaskDependency", back_populates="depending_task")
    # depended_by = relationship("TaskDependency", back_populates="depended_task")
    assignment = relationship("Assignment")
    enrollment = relationship("Enrollment")


class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)

    # relationships
    # depending_task = relationship("Task", back_populates="depends_on")
    # depended_task = relationship("Task", back_populates="depended_by")
