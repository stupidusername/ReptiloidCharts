"""
Create status table.

Revision ID: 12d4275947f9
Revises: 8f45d2d021c6
Create Date: 2018-11-01 18:15:11.337041
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12d4275947f9'
down_revision = '8f45d2d021c6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'entity_id',
            sa.Integer,
            sa.ForeignKey('entity.id'),
            nullable=False
        ),
        sa.Column('user_screen_name', sa.String(), nullable=False),
        sa.Column('status_id', sa.Integer, nullable=False, unique=True),
        sa.Column('create_datetime', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Text(), nullable=False),
        sa.Column('reply_count', sa.Integer, nullable=False),
        sa.Column('retweet_count', sa.Integer, nullable=False),
        sa.Column('favorite_count', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('status')
