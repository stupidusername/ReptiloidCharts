"""
Create entitiy table.

Revision ID: 8f45d2d021c6
Revises:
Create Date: 2018-11-01 18:08:05.985033
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f45d2d021c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'entitiy',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('screen_name', sa.String(), nullable=False),
        sa.Column('name', sa.String()),
        sa.Column('track', sa.Boolean),
        sa.Column('deleted', sa.Boolean),
    )


def downgrade():
    op.drop_table('entitiy')
