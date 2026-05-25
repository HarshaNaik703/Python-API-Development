"""modify user table name

Revision ID: 1769c649cad0
Revises: 51416949a3ef
Create Date: 2026-05-25 18:27:54.885191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1769c649cad0'
down_revision: Union[str, Sequence[str], None] = '51416949a3ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('uses','users')
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('users')
    """Downgrade schema."""
    pass
