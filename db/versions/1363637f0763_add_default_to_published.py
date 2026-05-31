from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1363637f0763'
down_revision: Union[str, Sequence[str], None] = 'c90034858bda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'posts',
        'published',
        existing_type=sa.Boolean(),
        server_default=sa.text('true'),
        existing_nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'posts',
        'published',
        existing_type=sa.Boolean(),
        server_default=None,
        existing_nullable=False
    )
