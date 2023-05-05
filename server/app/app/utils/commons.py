from sqlalchemy import Enum
import enum


class UserType(enum.Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class Priority(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TaskStatus(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"


class EnrollmentStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class WeekDay(enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
