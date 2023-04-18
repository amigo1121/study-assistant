from sqlalchemy import Enum
import enum


class UserType(enum.Enum):
    STUDENT = 1
    TEACHER = 2
