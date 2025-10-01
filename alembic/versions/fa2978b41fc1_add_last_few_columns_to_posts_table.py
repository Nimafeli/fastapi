"""add last few columns to posts table

Revision ID: fa2978b41fc1
Revises: d6125bca6a41
Create Date: 2025-09-28 19:01:30.601436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa2978b41fc1'
down_revision: Union[str, Sequence[str], None] = 'd6125bca6a41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, 
                                     server_default=sa.text('TRUE')))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('now()')))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    """Downgrade schema."""
    pass
