"""create meetups table

Revision ID: bd17190f4b0c
Revises: 
Create Date: 2022-02-11 17:21:07.406578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd17190f4b0c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "meetups",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("meetups")
    pass
