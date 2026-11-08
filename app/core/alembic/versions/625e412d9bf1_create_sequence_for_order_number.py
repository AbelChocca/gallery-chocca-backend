"""create sequence for order_number

Revision ID: 625e412d9bf1
Revises: 754a20969fdc
Create Date: 2026-10-04 19:06:46.660727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '625e412d9bf1'
down_revision: Union[str, Sequence[str], None] = '754a20969fdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE SEQUENCE order_number_seq START WITH 1 INCREMENT BY 1"
    )


def downgrade() -> None:
    op.execute(
        "DROP SEQUENCE IF EXISTS order_number_seq"
    )