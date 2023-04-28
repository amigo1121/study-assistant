from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Table,
    UniqueConstraint,
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

    def __repr__(self):
        return f"<Course(code='{self.code}', name='{self.name}', startDate='{self.startDate}', endDate='{self.endDate}', credit={self.credits})>"
