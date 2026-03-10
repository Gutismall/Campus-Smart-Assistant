"""remove sessions table

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-10

Drops the sessions table as JWTs are stateless.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the sessions table and its indexes
    op.drop_index('ix_sessions_id', table_name='sessions')
    op.drop_index('ix_sessions_token', table_name='sessions')
    op.drop_table('sessions')


def downgrade() -> None:
    # Re-create the sessions table if we ever need to go back
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_sessions_id', 'sessions', ['id'], unique=False)
    op.create_index('ix_sessions_token', 'sessions', ['token'], unique=True)
