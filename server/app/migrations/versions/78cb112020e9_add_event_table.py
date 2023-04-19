"""add event table

Revision ID: 78cb112020e9
Revises: 1eaff4afaee3
Create Date: 2023-04-19 07:16:10.705371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "78cb112020e9"
down_revision = "1eaff4afaee3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("start", sa.String(), nullable=False),
        sa.Column("end", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_event_id"), "event", ["id"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_event_id"), table_name="event")
    op.drop_table("event")
    # ### end Alembic commands ###