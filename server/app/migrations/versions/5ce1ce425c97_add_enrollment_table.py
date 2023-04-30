"""add enrollment table

Revision ID: 5ce1ce425c97
Revises: 11481f7b31a4
Create Date: 2023-04-29 23:17:01.059190

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import Enum
import enum


class EnrollmentStatus(enum.Enum):
    ACTIVE = 1
    DISABLED = 2


enrollment_status = postgresql.ENUM(EnrollmentStatus, name="enrollment_status")

# revision identifiers, used by Alembic.
revision = "5ce1ce425c97"
down_revision = "11481f7b31a4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("enrollment_date", sa.Date(), nullable=False),
        sa.UniqueConstraint(
            "student_id", "course_id", name="uq_student_course_enrollment"
        ),
    )
    enrollment_status.create(op.get_bind())

    op.add_column(
        "enrollments",
        sa.Column(
            "status",
            enrollment_status,
            nullable=False,
            server_default=EnrollmentStatus.ACTIVE.name,
        ),
    )


def downgrade() -> None:
    op.drop_table("enrollments")
    enrollment_status.drop(op.get_bind())
    pass
