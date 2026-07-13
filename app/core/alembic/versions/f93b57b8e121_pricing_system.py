"""pricing system

Revision ID: f93b57b8e121
Revises: f1bb5fe45efb
Create Date: 2026-05-26 19:40:07.318566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f93b57b8e121'
down_revision: Union[str, Sequence[str], None] = 'f1bb5fe45efb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column(
        "product",
        "price",
        new_column_name="base_price"
    )

    op.drop_column(
        "product",
        "discount_percentage"
    )

def downgrade() -> None:
    op.add_column(
        "product",
        sa.Column(
            "discount_percentage",
            sa.Numeric(5, 2),
            nullable=False,
            server_default=sa.text("0.00")
        )
    )

    op.alter_column(
        "product",
        "base_price",
        new_column_name="price"
    )