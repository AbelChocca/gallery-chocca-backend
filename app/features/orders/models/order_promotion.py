from decimal import Decimal

from sqlalchemy import (
    Column,
    Enum as SQLEnum,
)

from sqlmodel import Field, SQLModel
from app.features.pricing.types.promotion_types import PromotionApplicationScope

class OrderPromotionTable(SQLModel, table=True):
    __tablename__ = "order_promotions"

    id: int | None = Field(default=None, primary_key=True)

    order_id: int = Field(
        foreign_key="orders.id",
        index=True,
        nullable=False,
    )

    # Referencia a la promoción original
    promotion_id: int | None = Field(
        default=None,
        foreign_key="promotions.id",
        nullable=True,
    )

    # Snapshot
    name: str = Field(
        max_length=150,
        nullable=False,
    )

    application_scope: PromotionApplicationScope = Field(
        sa_column=Column(
            SQLEnum(
                PromotionApplicationScope,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
            ),
            nullable=False,
        ),
    )

    coupon_code: str | None = Field(
        default=None,
        max_length=50,
        nullable=True,
    )

    discount_amount: Decimal = Field(
        decimal_places=2,
        nullable=False,
    )