"""add course table

Revision ID: 792d0819f6b2
Revises: 15d948029767
Create Date: 2023-04-29 21:37:34.786771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "792d0819f6b2"
down_revision = "15d948029767"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column(
            "teacher_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )


def downgrade():
    op.drop_table("courses")
