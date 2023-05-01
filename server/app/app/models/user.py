from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.utils.commons import UserType
from app.utils.mixins import Timestamp
from .course import Enrollment


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserType), nullable=False)

    # relationship

    events = relationship("Event", back_populates="owner")
    registered_courses = relationship("Enrollment", back_populates="student")
    teaching_courses = relationship("Course", back_populates="teacher")
