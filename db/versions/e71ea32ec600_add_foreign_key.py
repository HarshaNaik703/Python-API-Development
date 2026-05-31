"""add foreign key

Revision ID: e71ea32ec600
Revises: 1769c649cad0
Create Date: 2026-05-25 18:31:09.556376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e71ea32ec600'
down_revision: Union[str, Sequence[str], None] = '1769c649cad0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['user_id'],ondelete='CASCADE')
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_constraint('posts_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    """Downgrade schema."""
    pass
