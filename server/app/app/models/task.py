from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from app.utils.commons import TaskStatus

Base = declarative_base()


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    est_hours = Column(Integer)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)


class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
