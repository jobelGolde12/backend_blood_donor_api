"""add theme preference to users

Revision ID: 002
Revises: 001
Create Date: 2026-02-06 18:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE themepreference AS ENUM ('light', 'dark', 'system')")
    op.add_column('users', sa.Column('theme_preference', sa.Enum('light', 'dark', 'system', name='themepreference'), nullable=False, server_default='system'))


def downgrade() -> None:
    op.drop_column('users', 'theme_preference')
    op.execute('DROP TYPE themepreference')
