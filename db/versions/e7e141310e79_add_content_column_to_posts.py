"""add content column to posts


Revision ID: e7e141310e79
Revises: 1c873bdc3e6a
Create Date: 2026-05-25 18:13:27.028779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7e141310e79'
down_revision: Union[str, Sequence[str], None] = '1c873bdc3e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    """Downgrade schema."""
    pass
