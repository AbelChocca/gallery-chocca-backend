from decimal import Decimal

from sqlalchemy import CheckConstraint, Column, Numeric
from sqlmodel import Field, SQLModel


class SaleItem(SQLModel, table=True):
    __tablename__ = "sale_item"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_sale_item_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_sale_item_unit_price_positive",
        ),
        CheckConstraint(
            "discount >= 0",
            name="ck_sale_item_discount_positive",
        ),
        CheckConstraint(
            "subtotal >= 0",
            name="ck_sale_item_subtotal_positive",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    sale_id: int = Field(
        foreign_key="sale.id",
        nullable=False,
    )

    variant_size_id: int = Field(
        foreign_key="variant_size.id",
        nullable=False,
    )

    quantity: int = Field(
        nullable=False,
    )

    unit_price: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
        )
    )

    discount: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
        )
    )

    subtotal: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
        )
    )

    cost: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(10, 2),
            nullable=True,
        )
    )