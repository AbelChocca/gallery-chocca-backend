"""rename variant_size_id column to owner_id and add owner_type in Inventory table, change unique constraint

Revision ID: e0c4c747e41f
Revises: 6d265912742e
Create Date: 2026-07-22 13:10:59.331745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0c4c747e41f'
down_revision: Union[str, Sequence[str], None] = '6d265912742e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from app.features.inventory.types.inventory_movement import InventoryOwnerType

inventory_owner_type = sa.Enum(
    InventoryOwnerType,
    name="inventory_owner_type",
)

def upgrade() -> None:
    # Crear el tipo ENUM
    inventory_owner_type.create(op.get_bind(), checkfirst=True)

    # Eliminar FK hacia variant_size
    op.drop_constraint(
        "inventory_variant_size_id_fkey",
        "inventory",
        type_="foreignkey",
    )

    # Renombrar variant_size_id -> owner_id
    op.alter_column(
        "inventory",
        "variant_size_id",
        new_column_name="owner_id",
    )

    # Agregar owner_type (nullable temporalmente)
    op.add_column(
        "inventory",
        sa.Column(
            "owner_type",
            inventory_owner_type,
            nullable=True,
        ),
    )

    # Todos los registros existentes son PRODUCT
    op.execute("""
        UPDATE inventory
        SET owner_type = 'PRODUCT'
        WHERE owner_type IS NULL
    """)

    # Convertir owner_type en NOT NULL
    op.alter_column(
        "inventory",
        "owner_type",
        nullable=False,
    )

    # Reemplazar UniqueConstraint
    op.drop_constraint(
        "uq_inventory_variant_size_location",
        "inventory",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_inventory_owner_location",
        "inventory",
        [
            "owner_type",
            "owner_id",
            "location_id",
        ],
    )


def downgrade() -> None:
    # Eliminar nuevo unique
    op.drop_constraint(
        "uq_inventory_owner_location",
        "inventory",
        type_="unique",
    )

    # Restaurar unique anterior
    op.create_unique_constraint(
        "uq_inventory_variant_size_location",
        "inventory",
        [
            "owner_id",
            "location_id",
        ],
    )

    # Eliminar owner_type
    op.drop_column(
        "inventory",
        "owner_type",
    )

    # Renombrar owner_id -> variant_size_id
    op.alter_column(
        "inventory",
        "owner_id",
        new_column_name="variant_size_id",
    )

    # Restaurar FK
    op.create_foreign_key(
        "inventory_variant_size_id_fkey",
        "inventory",
        "variant_size",
        ["variant_size_id"],
        ["id"],
    )

    # Eliminar el tipo ENUM
    inventory_owner_type.drop(op.get_bind(), checkfirst=True)