from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    credits = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Course(code='{self.code}', name='{self.name}', startDate='{self.startDate}', endDate='{self.endDate}', credit={self.credits})>"
