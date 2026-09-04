from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
)

from sqlmodel import Field, SQLModel


class CouponTable(SQLModel, table=True):
    __tablename__ = "coupons"

    __table_args__ = (
        CheckConstraint(
            "max_redemptions IS NULL OR max_redemptions >= 0",
            name="ck_coupon_max_redemptions_positive",
        ),
        CheckConstraint(
            """
            max_redemptions_per_customer IS NULL
            OR max_redemptions_per_customer >= 0
            """,
            name="ck_coupon_max_redemptions_customer_positive",
        ),
        CheckConstraint(
            "used_count >= 0",
            name="ck_coupon_used_count_positive",
        ),
        CheckConstraint(
            """
            ends_at IS NULL
            OR starts_at IS NULL
            OR ends_at > starts_at
            """,
            name="ck_coupon_valid_dates",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    promotion_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "promotions.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    code: str = Field(
        unique=True,
        index=True,
        max_length=100,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    starts_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    ends_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    max_redemptions: int | None = Field(
        default=None,
        nullable=True,
    )

    max_redemptions_per_customer: int | None = Field(
        default=None,
        nullable=True,
    )

    used_count: int = Field(
        default=0,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )