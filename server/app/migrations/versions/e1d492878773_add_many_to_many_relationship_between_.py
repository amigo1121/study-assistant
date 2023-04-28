"""Add many-to-many relationship between User and Course

Revision ID: e1d492878773
Revises: 0f3e259faf4a
Create Date: 2023-04-27 23:12:16.651986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e1d492878773"
down_revision = "0f3e259faf4a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "student_course",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "users", sa.Column("registered_courses", sa.ARRAY(sa.Integer()), nullable=True)
    )
    op.add_column(
        "courses", sa.Column("students", sa.ARRAY(sa.Integer()), nullable=True)
    )
    op.create_foreign_key(
        "fk_course_user",
        "student_course",
        "courses",
        ["course_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_user_course",
        "student_course",
        "users",
        ["student_id"],
        ["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("fk_user_course", "student_course", type_="foreignkey")
    op.drop_constraint("fk_course_user", "student_course", type_="foreignkey")
    op.drop_column("users", "registered_courses")
    op.drop_column("courses", "students")
    op.drop_table("student_course")
    pass
