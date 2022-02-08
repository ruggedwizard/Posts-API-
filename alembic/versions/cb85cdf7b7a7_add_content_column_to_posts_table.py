"""add content column to posts table

Revision ID: cb85cdf7b7a7
Revises: c9e6330d6e58
Create Date: 2022-02-08 01:38:29.275750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb85cdf7b7a7'
down_revision = 'c9e6330d6e58'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
