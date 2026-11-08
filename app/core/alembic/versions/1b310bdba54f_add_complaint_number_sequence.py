"""add complaint number sequence

Revision ID: 1b310bdba54f
Revises: 679def48f812
Create Date: 2026-10-29 22:47:18.802054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b310bdba54f'
down_revision: Union[str, Sequence[str], None] = '679def48f812'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS
            complaint_number_seq
        AS BIGINT
        START WITH 1
        INCREMENT BY 1
        NO CYCLE
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP SEQUENCE IF EXISTS complaint_number_seq"
    )