from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.utils.commons import UserType
from app.utils.mixins import Timestamp
from .course import student_course


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    type = Column(Enum(UserType), nullable=False)
    events = relationship("Event", back_populates="owner")
    registered_courses = relationship(
        "Course", secondary=student_course, back_populates="students"
    )
