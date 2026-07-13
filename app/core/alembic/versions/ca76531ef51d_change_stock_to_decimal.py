"""change stock to decimal

Revision ID: ca76531ef51d
Revises: 703380033472
Create Date: 2026-07-07 20:46:15.094622
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ca76531ef51d"
down_revision: Union[str, Sequence[str], None] = "703380033472"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "materials",
        "stock",
        existing_type=sa.Integer(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
        existing_server_default=sa.text("0"),
    )

    op.alter_column(
        "materials",
        "minimum_stock",
        existing_type=sa.Integer(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
        existing_server_default=sa.text("0"),
    )


def downgrade() -> None:
    op.alter_column(
        "materials",
        "stock",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Integer(),
        existing_nullable=False,
        existing_server_default=sa.text("0"),
    )

    op.alter_column(
        "materials",
        "minimum_stock",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Integer(),
        existing_nullable=False,
        existing_server_default=sa.text("0"),
    )