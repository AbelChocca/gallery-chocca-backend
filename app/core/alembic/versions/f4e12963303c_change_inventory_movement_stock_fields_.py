"""change inventory movement stock fields to decimal

Revision ID: f4e12963303c
Revises: ca76531ef51d
Create Date: 2026-07-07 23:26:14.704903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4e12963303c'
down_revision: Union[str, Sequence[str], None] = 'ca76531ef51d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "inventory_movement",
        "quantity",
        existing_type=sa.Integer(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
    )

    op.alter_column(
        "inventory_movement",
        "previous_stock",
        existing_type=sa.Integer(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
    )

    op.alter_column(
        "inventory_movement",
        "new_stock",
        existing_type=sa.Integer(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "inventory_movement",
        "quantity",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    op.alter_column(
        "inventory_movement",
        "previous_stock",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    op.alter_column(
        "inventory_movement",
        "new_stock",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Integer(),
        existing_nullable=False,
    )