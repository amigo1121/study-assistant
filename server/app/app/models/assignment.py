from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


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
