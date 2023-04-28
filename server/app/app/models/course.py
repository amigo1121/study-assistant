from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Table,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

student_course = Table(
    "student_course",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("student_id", ForeignKey("users.id")),
    Column("course_id", ForeignKey("courses.id")),
    UniqueConstraint("student_id", "course_id", name="uix_student_course"),
)


class CourseSchedule(Base):

    __tablename__ = "coursechedules"

    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    course = relationship("Course", back_populates="schedules")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    credits = Column(Integer, nullable=False)
    students = relationship(
        "User", secondary=student_course, back_populates="registered_courses"
    )
    teacher_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    teacher = relationship("User", back_populates="teaching_courses")
    schedules = relationship("CourseSchedule", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")

    def __repr__(self):
        return f"<Course(code='{self.code}', name='{self.name}', startDate='{self.startDate}', endDate='{self.endDate}', credit={self.credits})>"


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    course = relationship("Course", back_populates="assignments")
