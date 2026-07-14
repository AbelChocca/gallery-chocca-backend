from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Numeric,
    UniqueConstraint,
)
from sqlmodel import Field, SQLModel

class VariantSizeMaterialTable(SQLModel, table=True):
    __tablename__ = "variant_size_materials"

    __table_args__ = (
        UniqueConstraint(
            "variant_size_id",
            "material_id",
            name="uq_variant_size_material"
        ),
        Index(
            "ix_variant_size_material_variant_size_id",
            "variant_size_id"
        ),
        Index(
            "ix_variant_size_material_material_id",
            "material_id"
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_variant_size_material_quantity_positive"
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    variant_size_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "variant_sizes.id",
                ondelete="CASCADE"
            ),
            nullable=False
        )
    )

    material_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "materials.id",
                ondelete="RESTRICT"
            ),
            nullable=False
        )
    )

    quantity: Decimal = Field(
        sa_column=Column(
            Numeric(12, 2),
            nullable=False
        )
    )