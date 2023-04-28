"""add Assignment table and relation ship with course

Revision ID: cff33e41edab
Revises: d105f0b4f555
Create Date: 2023-04-28 09:55:02.412794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cff33e41edab"
down_revision = "d105f0b4f555"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("priority", sa.String(50), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("due_date", sa.DateTime, nullable=False),
        sa.Column(
            "course_id",
            sa.Integer,
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.create_foreign_key(
        "fk_assignments_course_id", "assignments", "courses", ["course_id"], ["id"]
    )
    pass


def downgrade() -> None:
    op.drop_constraint("fk_assignments_course_id", "assignments", type_="foreignkey")
    op.drop_table("assignments")
    pass
