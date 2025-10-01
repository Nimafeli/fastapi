"""add content column to posts table

Revision ID: e5cc2dcc2883
Revises: 180e646dff39
Create Date: 2025-09-28 18:22:17.466671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5cc2dcc2883'
down_revision: Union[str, Sequence[str], None] = '180e646dff39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
