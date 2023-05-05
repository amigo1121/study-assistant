"""add priority for task

Revision ID: a4ff2a85c195
Revises: ab4a761884eb
Create Date: 2023-05-05 11:51:57.930363

"""
from alembic import op
import sqlalchemy as sa
from app.utils.commons import Priority
from sqlalchemy.dialects import postgresql

task_priority = postgresql.ENUM(Priority, name="task_priority")


# revision identifiers, used by Alembic.
revision = "a4ff2a85c195"
down_revision = "ab4a761884eb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    task_priority.create(op.get_bind())

    op.add_column(
        "tasks",
        sa.Column(
            "priority", task_priority, nullable=False, server_default=Priority.LOW.name
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("tasks", "priority")
    task_priority.drop(op.get_bind())
    pass
