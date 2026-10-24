"""update inventory movement type and reference type enums

Revision ID: ed3bd4e32c6a
Revises: 625e412d9bf1
Create Date: 2026-10-11 21:19:57.955645

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ed3bd4e32c6a'
down_revision: Union[str, Sequence[str], None] = '625e412d9bf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # inventory_movement_type
    op.execute(
        """
        ALTER TYPE inventory_movement_type
        ADD VALUE IF NOT EXISTS 'RESERVATION'
        """
    )

    op.execute(
        """
        ALTER TYPE inventory_movement_type
        ADD VALUE IF NOT EXISTS 'RESERVATION_RELEASE'
        """
    )

    # inventory_reference_type
    op.execute(
        """
        ALTER TYPE inventory_reference_type
        ADD VALUE IF NOT EXISTS 'ORDER'
        """
    )


def downgrade() -> None:
    # IMPORTANT:
    # El downgrade solo funcionará si no existen filas usando
    # RESERVATION / RESERVATION_RELEASE / ORDER.

    # -------------------------
    # inventory_movement_type
    # -------------------------

    op.execute(
        """
        ALTER TYPE inventory_movement_type
        RENAME TO inventory_movement_type_old
        """
    )

    op.execute(
        """
        CREATE TYPE inventory_movement_type AS ENUM (
            'ENTRY',
            'MANUAL_ADJUSTMENT',
            'USAGE',
            'SALE',
            'CUSTOMER_RETURN',
            'SUPPLIER_RETURN',
            'TRANSFER'
        )
        """
    )

    op.execute(
        """
        ALTER TABLE inventory_movement
        ALTER COLUMN type
        TYPE inventory_movement_type
        USING type::text::inventory_movement_type
        """
    )

    op.execute(
        """
        DROP TYPE inventory_movement_type_old
        """
    )

    # -------------------------
    # inventory_reference_type
    # -------------------------

    op.execute(
        """
        ALTER TYPE inventory_reference_type
        RENAME TO inventory_reference_type_old
        """
    )

    op.execute(
        """
        CREATE TYPE inventory_reference_type AS ENUM (
            'SALE',
            'STOCK_TRANSFER',
            'PRODUCTION_ORDER',
            'PURCHASE',
            'MANUAL_ADJUSTMENT',
            'CUSTOMER_RETURN',
            'SUPPLIER_RETURN'
        )
        """
    )

    op.execute(
        """
        ALTER TABLE inventory_movement
        ALTER COLUMN reference_type
        TYPE inventory_reference_type
        USING reference_type::text::inventory_reference_type
        """
    )

    op.execute(
        """
        DROP TYPE inventory_reference_type_old
        """
    )