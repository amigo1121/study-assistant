"""add schedules table

Revision ID: 11481f7b31a4
Revises: 792d0819f6b2
Create Date: 2023-04-29 22:43:06.321491

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import Enum
import enum


class Weekday(enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


# revision identifiers, used by Alembic.
revision = "11481f7b31a4"
down_revision = "792d0819f6b2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "course_schedule",
        sa.Column("schedule_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "course_id", sa.Integer(), sa.ForeignKey("courses.id"), nullable=False
        ),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
    )

    week_day = postgresql.ENUM(Weekday, name="weekday")
    week_day.create(op.get_bind())
    op.add_column("course_schedule", sa.Column("week_day", week_day, nullable=False))


def downgrade():
    op.drop_table("course_schedule")
    week_day = postgresql.ENUM(Weekday, name="weekday")
    week_day.drop(op.get_bind())
