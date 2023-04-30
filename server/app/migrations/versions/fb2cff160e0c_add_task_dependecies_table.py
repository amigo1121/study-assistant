"""add task dependecies table

Revision ID: fb2cff160e0c
Revises: addd5fff895f
Create Date: 2023-04-30 01:33:44.341027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fb2cff160e0c"
down_revision = "addd5fff895f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "task_dependencies",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "task_id",
            sa.Integer(),
            sa.ForeignKey("tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "depend_on_task_id",
            sa.Integer(),
            sa.ForeignKey("tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.UniqueConstraint("task_id", "depend_on_task_id", name="uq_task_dependent"),
    )


def downgrade():
    op.drop_table("task_dependencies")
