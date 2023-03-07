"""add description to meetups

Revision ID: 793d76ce923c
Revises: bd17190f4b0c
Create Date: 2022-02-11 17:33:32.358726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "793d76ce923c"
down_revision = "bd17190f4b0c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("meetups", sa.Column("description", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("meetups", "description")
    pass
