from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    est_hours = Column(Integer)
    due_date = Column(Date)
    due_time = Column(Time)
    dependencies = relationship(
        "Task",
        secondary="taskdependencies",
        primaryjoin="Task.id==taskdependencies.c.task_id",
        secondaryjoin="Task.id==taskdependencies.c.depends_on_id",
        backref="dependent_tasks",
    )


class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    depends_on_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
