"""Se agregao columna 'slug' a la Tabla Product

Revision ID: 0e6eadc205ca
Revises: 
Create Date: 2025-12-09 18:15:19.832131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0e6eadc205ca'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # NO-OP: la columna slug ya existe en la DB
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # NO-OP
    pass