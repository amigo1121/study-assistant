from .user import User, UserCreate, UserLogin, UserChangePassword
from .event import (
    EventCreate,
    MultilpleEventCreate,
    EventBase,
    Event,
    EventUpdate,
    EventDelete,
)
from .course import CourseCreate, CourseRead, CourseUpdate
from .enrollment import StudentWithCourse, CourseWithStudent, EnrollmentBase
from .course_action import LeaveCourse, RegisterCourse, StudentCourseInfo
from .assignment import (
    AssignmentCreate,
    Assignment,
    AssignmentUpdate,
    AssignmentWithTaks,
    AssignmentWithTaskSummary,
)
from .task import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskDependencyBase,
    TaskDependencyCreate,
    TaskDependency,
    TaskWithDepdend,
    TaskUpdateStatus,
    TaskWithAssignmentID,
)
