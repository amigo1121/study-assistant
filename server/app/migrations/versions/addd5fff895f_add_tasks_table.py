"""add tasks table

Revision ID: addd5fff895f
Revises: c5f4c03acb48
Create Date: 2023-04-30 00:38:38.286636

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum
from sqlalchemy.dialects import postgresql
import enum


class TaskStatus(enum.Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETE = 3


task_status = postgresql.ENUM(TaskStatus, name="task_status")

# revision identifiers, used by Alembic.
revision = "addd5fff895f"
down_revision = "c5f4c03acb48"
branch_labels = None
depends_on = None


def upgrade() -> None:

    task_status.create(op.get_bind())
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("est_hours", sa.Integer(), nullable=False),
        sa.Column(
            "enrollment_id",
            sa.Integer(),
            sa.ForeignKey("enrollments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "assignment_id",
            sa.Integer(),
            sa.ForeignKey("assignments.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "status",
            task_status,
            nullable=False,
            server_default=TaskStatus.NOT_STARTED.name,
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("tasks"),
    task_status.drop(op.get_bind())
    pass
