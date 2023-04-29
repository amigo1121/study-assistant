"""add user table

Revision ID: 15d948029767
Revises:
Create Date: 2023-04-29 20:56:30.034598

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "15d948029767"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("password_hash"),
    )

    user_type = postgresql.ENUM("STUDENT", "TEACHER", name="user_type")
    user_type.create(op.get_bind())
    op.add_column(
        "users",
        sa.Column(
            "role", sa.Enum("STUDENT", "TEACHER", name="user_type"), nullable=False
        ),
    )
    pass


def downgrade():
    op.drop_table("users")
    user_type = postgresql.ENUM("STUDENT", "TEACHER", name="user_type")
    user_type.drop(op.get_bind())
