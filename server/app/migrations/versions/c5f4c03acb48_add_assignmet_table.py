"""add assignmet table

Revision ID: c5f4c03acb48
Revises: 5ce1ce425c97
Create Date: 2023-04-30 00:10:21.915453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c5f4c03acb48"
down_revision = "5ce1ce425c97"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "due_date", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("assignments")
    pass
