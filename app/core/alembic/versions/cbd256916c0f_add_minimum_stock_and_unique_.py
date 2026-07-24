"""add minimum stock and unique restriction on sku column in Variant Size Table

Revision ID: cbd256916c0f
Revises: 74f28f4520c9
Create Date: 2026-07-14 23:02:21.456653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cbd256916c0f'
down_revision: Union[str, Sequence[str], None] = '74f28f4520c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Add minimum_stock column
    op.add_column(
        "variant_size",
        sa.Column(
            "minimum_stock",
            sa.Integer(),
            nullable=False,
            server_default="0"
        )
    )


    # Add unique constraint for sku
    op.create_unique_constraint(
        "uq_variant_size_sku",
        "variant_size",
        ["sku"]
    )


def downgrade() -> None:

    # Remove unique constraint
    op.drop_constraint(
        "uq_variant_size_sku",
        "variant_size",
        type_="unique"
    )


    # Remove minimum_stock column
    op.drop_column(
        "variant_size",
        "minimum_stock"
    )
