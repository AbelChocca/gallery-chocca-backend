"""add barcode column in VariantSizeTable and remove stock and minimun_stock columns

Revision ID: 6d265912742e
Revises: cbd256916c0f
Create Date: 2026-07-18 14:45:47.464584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d265912742e'
down_revision: Union[str, Sequence[str], None] = 'cbd256916c0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("variant_size", "stock")
    op.drop_column("variant_size", "minimum_stock")

    op.add_column(
        "variant_size",
        sa.Column("barcode", sa.String(length=100), nullable=True),
    )

    op.create_unique_constraint(
        "uq_variant_size_barcode",
        "variant_size",
        ["barcode"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_variant_size_barcode",
        "variant_size",
        type_="unique",
    )

    op.drop_column("variant_size", "barcode")

    op.add_column(
        "variant_size",
        sa.Column(
            "minimum_stock",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "variant_size",
        sa.Column(
            "stock",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.alter_column("variant_size", "stock", server_default=None)
    op.alter_column("variant_size", "minimum_stock", server_default=None)
