"""remove stock and minimum stock from material table

Revision ID: 71bfa48d7078
Revises: 961c2ec3dab2
Create Date: 2026-07-24 16:47:50.369306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71bfa48d7078'
down_revision: Union[str, Sequence[str], None] = '961c2ec3dab2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column(
        "materials",
        "stock"
    )

    op.drop_column(
        "materials",
        "minimum_stock"
    )


def downgrade() -> None:
    op.add_column(
        "materials",
        sa.Column(
            "stock",
            sa.Numeric(
                precision=10,
                scale=2
            ),
            nullable=False,
            server_default="0.00"
        )
    )

    op.add_column(
        "materials",
        sa.Column(
            "minimum_stock",
            sa.Numeric(
                precision=10,
                scale=2
            ),
            nullable=False,
            server_default="0.00"
        )
    )