from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .user import User
from app.db.base_class import Base


class Event(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)
    owner = relationship("User", back_populates="events")
