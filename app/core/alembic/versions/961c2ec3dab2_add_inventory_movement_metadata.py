"""add inventory movement metadata

Revision ID: 961c2ec3dab2
Revises: e0c4c747e41f
Create Date: 2026-07-22 18:32:09.640531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.features.inventory.types.inventory_reference import InventoryReferenceType


# revision identifiers, used by Alembic.
revision: str = '961c2ec3dab2'
down_revision: Union[str, Sequence[str], None] = 'e0c4c747e41f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # -------------------------
    # Columns
    # -------------------------

    op.add_column(
        "inventory_movement",
        sa.Column(
            "location_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "inventory_movement",
        sa.Column(
            "performed_by",
            sa.Integer(),
            nullable=True,
        ),
    )

    reference_type_enum = sa.Enum(
        InventoryReferenceType,
        name="inventory_reference_type",
    )

    reference_type_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "inventory_movement",
        sa.Column(
            "reference_type",
            reference_type_enum,
            nullable=True,
        ),
    )

    op.add_column(
        "inventory_movement",
        sa.Column(
            "reference_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # -------------------------
    # Foreign Keys
    # -------------------------

    op.create_foreign_key(
        "fk_inventory_movement_location",
        "inventory_movement",
        "inventory_location",
        ["location_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_inventory_movement_performed_by",
        "inventory_movement",
        "usertable",
        ["performed_by"],
        ["id"],
    )

    # -------------------------
    # Indexes
    # -------------------------

    op.create_index(
        "ix_inventory_movement_location",
        "inventory_movement",
        ["location_id"],
    )

    op.create_index(
        "ix_inventory_movement_created_at",
        "inventory_movement",
        ["created_at"],
    )


def downgrade() -> None:
    # -------------------------
    # Indexes
    # -------------------------

    op.drop_index(
        "ix_inventory_movement_created_at",
        table_name="inventory_movement",
    )

    op.drop_index(
        "ix_inventory_movement_location",
        table_name="inventory_movement",
    )

    # -------------------------
    # Foreign Keys
    # -------------------------

    op.drop_constraint(
        "fk_inventory_movement_performed_by",
        "inventory_movement",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_inventory_movement_location",
        "inventory_movement",
        type_="foreignkey",
    )

    # -------------------------
    # Columns
    # -------------------------

    op.drop_column(
        "inventory_movement",
        "reference_id",
    )

    op.drop_column(
        "inventory_movement",
        "reference_type",
    )

    op.drop_column(
        "inventory_movement",
        "performed_by",
    )

    op.drop_column(
        "inventory_movement",
        "location_id",
    )

    # -------------------------
    # Enum
    # -------------------------

    sa.Enum(
        InventoryReferenceType,
        name="inventory_reference_type",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )
