"""completing posts table

Revision ID: 105ed2e46f0e
Revises: e71ea32ec600
Create Date: 2026-05-25 19:27:28.027620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '105ed2e46f0e'
down_revision: Union[str, Sequence[str], None] = 'e71ea32ec600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean,server_default=True, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    """Downgrade schema."""
    pass
