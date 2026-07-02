from decimal import Decimal

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import (
    ForeignKey,
    Numeric,
    UniqueConstraint,
    Index,
    CheckConstraint
)


class ProductMaterialTable(SQLModel, table=True):
    __tablename__ = "product_materials"

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "material_id",
            name="uq_product_material_product_material"
        ),
        Index(
            "ix_product_material_product_id",
            "product_id"
        ),
        Index(
            "ix_product_material_material_id",
            "material_id"
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_product_material_quantity_positive"
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    product_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "products.id",
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