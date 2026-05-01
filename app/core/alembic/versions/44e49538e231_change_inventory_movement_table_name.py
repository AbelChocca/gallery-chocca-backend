"""change inventory movement table name

Revision ID: 44e49538e231
Revises: 18a5d418d133
Create Date: 2026-04-28 01:19:04.645768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '44e49538e231'
down_revision: Union[str, Sequence[str], None] = '18a5d418d133'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table("inventorymovementtable", "inventory_movement")

def downgrade():
    op.rename_table("inventory_movement", "inventorymovementtable")
