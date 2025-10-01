"""add foreign-key to posts table

Revision ID: d6125bca6a41
Revises: 4cd679d82b68
Create Date: 2025-09-28 18:53:02.933636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6125bca6a41'
down_revision: Union[str, Sequence[str], None] = '4cd679d82b68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    """Downgrade schema."""
    pass
