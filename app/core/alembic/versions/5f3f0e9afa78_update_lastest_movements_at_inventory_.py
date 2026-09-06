"""update lastest movements at Inventory column

Revision ID: 5f3f0e9afa78
Revises: 5b386d95ff88
Create Date: 2026-09-06 03:40:12.974816

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5f3f0e9afa78'
down_revision: Union[str, Sequence[str], None] = '5b386d95ff88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE inventory AS i
        SET last_movement_at = latest.created_at
        FROM (
            SELECT DISTINCT ON (
                owner_type,
                owner_id,
                location_id
            )
                owner_type,
                owner_id,
                location_id,
                created_at
            FROM inventory_movement
            ORDER BY
                owner_type,
                owner_id,
                location_id,
                created_at DESC
        ) AS latest
        WHERE
            i.owner_type = latest.owner_type
            AND i.owner_id = latest.owner_id
            AND i.location_id = latest.location_id;
        """
    )


def downgrade() -> None:
    pass