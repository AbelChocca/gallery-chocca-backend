"""add locations link inventory location

Revision ID: 679def48f812
Revises: ed3bd4e32c6a
Create Date: 2026-10-12 21:42:54.121257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '679def48f812'
down_revision: Union[str, Sequence[str], None] = 'ed3bd4e32c6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # --------------------------------
    # locations
    # --------------------------------

    op.create_table(
        "locations",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
        ),

        sa.Column(
            "type",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "address",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "ubigeo_code",
            sa.String(length=6),
            nullable=True,
        ),

        sa.Column(
            "latitude",
            sa.Numeric(9, 6),
            nullable=True,
        ),

        sa.Column(
            "longitude",
            sa.Numeric(9, 6),
            nullable=True,
        ),

        sa.Column(
            "phone",
            sa.String(length=30),
            nullable=True,
        ),

        sa.Column(
            "reference",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "external_provider",
            sa.String(length=50),
            nullable=True,
        ),

        sa.Column(
            "external_code",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),

        sa.ForeignKeyConstraint(
            ["ubigeo_code"],
            ["ubigeos.code"],
            name="fk_locations_ubigeo_code",
        ),

        sa.CheckConstraint(
            """
            type IN (
                'STORE',
                'WORKSHOP',
                'WAREHOUSE',
                'CARRIER_PICKUP',
                'OTHER'
            )
            """,
            name="ck_locations_type",
        ),
    )

    op.create_index(
        "ix_locations_name",
        "locations",
        ["name"],
    )

    op.create_index(
        "ix_locations_ubigeo_code",
        "locations",
        ["ubigeo_code"],
    )

    op.create_index(
        "ix_locations_external_provider",
        "locations",
        ["external_provider"],
    )

    op.create_index(
        "ix_locations_external_code",
        "locations",
        ["external_code"],
    )

    op.create_index(
        "ix_locations_is_active",
        "locations",
        ["is_active"],
    )

    # --------------------------------
    # inventory_location
    # --------------------------------

    op.add_column(
        "inventory_location",
        sa.Column(
            "location_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_inventory_location_location_id",
        "inventory_location",
        "locations",
        ["location_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_index(
        "ix_inventory_location_location_id",
        "inventory_location",
        ["location_id"],
        unique=True,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_inventory_location_location_id",
        table_name="inventory_location",
    )

    op.drop_constraint(
        "fk_inventory_location_location_id",
        "inventory_location",
        type_="foreignkey",
    )

    op.drop_column(
        "inventory_location",
        "location_id",
    )

    op.drop_index(
        "ix_locations_is_active",
        table_name="locations",
    )

    op.drop_index(
        "ix_locations_external_code",
        table_name="locations",
    )

    op.drop_index(
        "ix_locations_external_provider",
        table_name="locations",
    )

    op.drop_index(
        "ix_locations_ubigeo_code",
        table_name="locations",
    )

    op.drop_index(
        "ix_locations_name",
        table_name="locations",
    )

    op.drop_table(
        "locations"
    )