"""add owner_name and owner_code columns to Inventory Movements table

Revision ID: 30b1098131ba
Revises: 8ab9581fe7d2
Create Date: 2026-06-18 01:09:00.754411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '30b1098131ba'
down_revision: Union[str, Sequence[str], None] = '8ab9581fe7d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "inventory_movement",
        sa.Column(
            "owner_code",
            sa.String(length=100),
            nullable=False
        )
    )

    op.add_column(
        "inventory_movement",
        sa.Column(
            "owner_name",
            sa.String(length=255),
            nullable=False
        )
    )

    op.create_index(
        "ix_inventory_movement_owner",
        "inventory_movement",
        ["owner_type", "owner_id"],
        unique=False
    )

    op.create_index(
        "ix_inventory_movement_owner_code",
        "inventory_movement",
        ["owner_code"],
        unique=False
    )

    op.create_index(
        "ix_inventory_movement_owner_name",
        "inventory_movement",
        ["owner_name"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        "ix_inventory_movement_owner_name",
        table_name="inventory_movement"
    )

    op.drop_index(
        "ix_inventory_movement_owner_code",
        table_name="inventory_movement"
    )

    op.drop_index(
        "ix_inventory_movement_owner",
        table_name="inventory_movement"
    )

    op.drop_column(
        "inventory_movement",
        "owner_name"
    )

    op.drop_column(
        "inventory_movement",
        "owner_code"
    )
