"""update inventory movement type

Revision ID: 1bb3c0ebee14
Revises: 9f3a213adb87
Create Date: 2026-06-20 02:23:55.057157

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1bb3c0ebee14'
down_revision: Union[str, Sequence[str], None] = '9f3a213adb87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TYPE inventory_movement_type
        RENAME TO inventory_movement_type_old;
    """)

    op.execute("""
        CREATE TYPE inventory_movement_type AS ENUM (
            'entry',
            'manual_adjustment',
            'sale',
            'customer_return',
            'supplier_return'
        );
    """)

    op.execute("""
        ALTER TABLE inventory_movement
        ALTER COLUMN type
        TYPE inventory_movement_type
        USING type::text::inventory_movement_type;
    """)

    op.execute("""
        DROP TYPE inventory_movement_type_old;
    """)


def downgrade():
    op.execute("""
        ALTER TYPE inventory_movement_type
        RENAME TO inventory_movement_type_new;
    """)

    op.execute("""
        CREATE TYPE inventory_movement_type AS ENUM (
            'RESTOCK',
            'MANUAL_ADJUSTMENT',
            'SALE',
            'RETURN'
        );
    """)

    op.execute("""
        ALTER TABLE inventory_movement
        ALTER COLUMN type
        TYPE inventory_movement_type
        USING type::text::inventory_movement_type;
    """)

    op.execute("""
        DROP TYPE inventory_movement_type_new;
    """)