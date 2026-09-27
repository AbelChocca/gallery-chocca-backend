"""delete pricing rule table legacy and product pricing rules table

Revision ID: 754a20969fdc
Revises: 5f3f0e9afa78
Create Date: 2026-09-23 03:33:03.786736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '754a20969fdc'
down_revision: Union[str, Sequence[str], None] = '5f3f0e9afa78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("product_pricing_rules")
    op.drop_table("pricing_rules")


def downgrade() -> None:
    pass
