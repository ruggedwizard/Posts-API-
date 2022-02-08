"""added last few columns to  post table

Revision ID: 303505fe2bf4
Revises: e74ad412ebb2
Create Date: 2022-02-08 02:12:47.415516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '303505fe2bf4'
down_revision = 'e74ad412ebb2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False, server_default='TRUE'),
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),))
    pass


def downgrade():
    pass
