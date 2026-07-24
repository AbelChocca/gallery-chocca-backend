"""add variant size material table and remove product material table

Revision ID: 74f28f4520c9
Revises: f4e12963303c
Create Date: 2026-07-14 16:42:53.980289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '74f28f4520c9'
down_revision: Union[str, Sequence[str], None] = 'f4e12963303c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    conn = op.get_bind()


    # ---------------------------------
    # Remove old tables if they exist
    # ---------------------------------

    old_tables = [
        "product_materials",
        "product_material",
    ]

    for table in old_tables:

        exists = conn.execute(
            sa.text(
                """
                SELECT to_regclass(:table_name)
                """
            ),
            {
                "table_name": table
            }
        ).scalar()

        if exists:
            op.drop_table(
                table
            )


    # ---------------------------------
    # Create variant_size_materials
    # ---------------------------------

    op.create_table(
        "variant_size_materials",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "variant_size_id",
            sa.Integer(),
            sa.ForeignKey(
                "variant_size.id",
                ondelete="CASCADE"
            ),
            nullable=False
        ),

        sa.Column(
            "material_id",
            sa.Integer(),
            sa.ForeignKey(
                "materials.id",
                ondelete="RESTRICT"
            ),
            nullable=False
        ),

        sa.Column(
            "quantity",
            sa.Numeric(
                precision=12,
                scale=2
            ),
            nullable=False
        ),

        sa.UniqueConstraint(
            "variant_size_id",
            "material_id",
            name="uq_variant_size_material"
        ),

        sa.CheckConstraint(
            "quantity > 0",
            name="ck_variant_size_material_quantity_positive"
        )
    )


    # ---------------------------------
    # Indexes
    # ---------------------------------

    op.create_index(
        "ix_variant_size_material_variant_size_id",
        "variant_size_materials",
        ["variant_size_id"]
    )

    op.create_index(
        "ix_variant_size_material_material_id",
        "variant_size_materials",
        ["material_id"]
    )



def downgrade() -> None:

    op.drop_index(
        "ix_variant_size_material_material_id",
        table_name="variant_size_materials"
    )

    op.drop_index(
        "ix_variant_size_material_variant_size_id",
        table_name="variant_size_materials"
    )


    op.drop_table(
        "variant_size_materials"
    )