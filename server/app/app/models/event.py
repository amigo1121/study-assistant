from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .user import User
from app.db.base_class import Base


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    start = Column(String)
    end = Column(String)
    owner = relationship("User", back_populates="events")
