from decimal import Decimal

from sqlmodel import Field, SQLModel


class OrderItemTable(SQLModel, table=True):
    __tablename__ = "order_items"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    order_id: int = Field(
        foreign_key="orders.id",
        nullable=False,
        index=True,
    )

    # Referencias al catálogo
    product_id: int | None = Field(
        default=None,
        foreign_key="product.id",
        nullable=True,
    )

    variant_id: int | None = Field(
        default=None,
        foreign_key="variant.id",
        nullable=True,
    )

    variant_size_id: int | None = Field(
        default=None,
        foreign_key="variant_size.id",
        nullable=True,
    )

    # Snapshot del producto
    product_name: str = Field(
        max_length=200,
        nullable=False,
    )

    sku: str = Field(
        max_length=100,
        nullable=False,
    )

    color: str | None = Field(
        default=None,
        max_length=100,
    )

    size: str | None = Field(
        default=None,
        max_length=50,
    )

    quantity: int = Field(
        nullable=False,
    )

    unit_original_price: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    unit_final_price: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    discount_amount: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    original_total: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )

    final_total: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        nullable=False,
    )