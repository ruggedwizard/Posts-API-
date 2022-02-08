"""add users table

Revision ID: d5fba1298795
Revises: cb85cdf7b7a7
Create Date: 2022-02-08 01:44:35.392763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5fba1298795'
down_revision = 'cb85cdf7b7a7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
    sa.Column('id',sa.Integer(), nullable=False),
    sa.Column('email',sa.String(), nullable=False),
    sa.Column('password',sa.String(),nullable=False), 
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
