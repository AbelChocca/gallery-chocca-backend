"""add usage to inventory movement type

Revision ID: 703380033472
Revises: 681cc614f2ff
Create Date: 2026-07-05 18:15:10.851595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '703380033472'
down_revision: Union[str, Sequence[str], None] = '681cc614f2ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TYPE inventory_movement_type ADD VALUE 'USAGE';
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
