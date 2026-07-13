"""add owner_type and owner_id and delete variant_size_id column to InventoryMovement Table

Revision ID: 8ab9581fe7d2
Revises: da0bc75361de
Create Date: 2026-06-11 04:12:46.590827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8ab9581fe7d2'
down_revision: Union[str, Sequence[str], None] = 'da0bc75361de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:
    # Crear enum nuevo
    inventory_owner_type = sa.Enum(
        "PRODUCT",
        "MATERIAL",
        name="inventory_owner_type"
    )
    inventory_owner_type.create(op.get_bind(), checkfirst=True)

    # Agregar columnas nuevas
    op.add_column(
        "inventory_movement",
        sa.Column(
            "owner_type",
            inventory_owner_type,
            nullable=False
        )
    )

    op.add_column(
        "inventory_movement",
        sa.Column(
            "owner_id",
            sa.Integer(),
            nullable=False
        )
    )

    # Eliminar columna antigua
    op.drop_column(
        "inventory_movement",
        "variant_size_id"
    )


def downgrade() -> None:
    # Restaurar columna antigua
    op.add_column(
        "inventory_movement",
        sa.Column(
            "variant_size_id",
            sa.Integer(),
            nullable=False
        )
    )

    # Eliminar columnas nuevas
    op.drop_column(
        "inventory_movement",
        "owner_id"
    )

    op.drop_column(
        "inventory_movement",
        "owner_type"
    )

    # Eliminar enum
    inventory_owner_type = sa.Enum(
        "PRODUCT",
        "MATERIAL",
        name="inventory_owner_type"
    )
    inventory_owner_type.drop(op.get_bind(), checkfirst=True)
