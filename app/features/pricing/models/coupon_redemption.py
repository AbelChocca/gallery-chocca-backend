from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
)

from sqlmodel import Field, SQLModel

class CouponRedemptionTable(SQLModel, table=True):
    __tablename__ = "coupon_redemptions"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    coupon_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "coupons.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    customer_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "customer.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
            index=True,
        )
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )