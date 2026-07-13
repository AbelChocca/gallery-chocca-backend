"""add material value to image_owner_type

Revision ID: 9f3a213adb87
Revises: 30b1098131ba
Create Date: 2026-06-20 01:58:57.755331

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9f3a213adb87'
down_revision: Union[str, Sequence[str], None] = '30b1098131ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        "ALTER TYPE image_owner_type ADD VALUE 'material';"
    )


def downgrade():
    pass