"""add check constraint enum user role

Revision ID: 681cc614f2ff
Revises: f581a43119e6
Create Date: 2026-06-27 00:49:38.436411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '681cc614f2ff'
down_revision: Union[str, Sequence[str], None] = 'f581a43119e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.alter_column(
        "usertable",
        "role",
        existing_type=sa.String(length=20),
        type_=sa.Enum(
            "admin",
            "manager",
            "seller",
            "inventory",
            "accountant",
            "user",
            name="user_role",
            native_enum=False,
            create_constraint=True,
        ),
        existing_nullable=False,
    )


def downgrade():

    op.alter_column(
        "usertable",
        "role",
        existing_type=sa.Enum(
            "admin",
            "manager",
            "seller",
            "inventory",
            "accountant",
            "user",
            name="user_role",
            native_enum=False,
            create_constraint=True,
        ),
        type_=sa.String(length=20),
        existing_nullable=False,
    )
