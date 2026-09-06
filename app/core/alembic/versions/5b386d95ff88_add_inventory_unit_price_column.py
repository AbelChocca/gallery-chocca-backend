"""add inventory unit_price column

Revision ID: 5b386d95ff88
Revises: 28617aa4883e
Create Date: 2026-09-05 00:20:06.503697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b386d95ff88'
down_revision: Union[str, Sequence[str], None] = '28617aa4883e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "inventory",
        sa.Column(
            "unit_price",
            sa.Numeric(12, 2),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "inventory",
        "unit_price",
    )