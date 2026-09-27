from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum as SQLEnum,
    Text,
)

from sqlmodel import Field, SQLModel
from app.features.sales.types.sale import SaleChannel
from app.features.pricing.types.promotion_types import PromotionStackingMode, PromotionApplicationScope


class PromotionTable(SQLModel, table=True):
    __tablename__ = "promotions"

    __table_args__ = (
        CheckConstraint(
            "priority >= 0",
            name="ck_promotion_priority_positive",
        ),
        CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at > starts_at",
            name="ck_promotion_valid_dates",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=255,
        nullable=False,
        index=True,
    )

    description: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    sales_channel: SaleChannel = Field(
        sa_column=Column(
            SQLEnum(
                SaleChannel,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        )
    )

    stacking_mode: PromotionStackingMode = Field(
        sa_column=Column(
            SQLEnum(
                PromotionStackingMode,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        )
    )

    application_scope: PromotionApplicationScope = Field(
        default=PromotionApplicationScope.PER_ITEM,
        sa_column=Column(
            SQLEnum(
                PromotionApplicationScope,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="promotion_application_scope",
            ),
            nullable=False,
            server_default=PromotionApplicationScope.PER_ITEM.value,
        ),
    )

    priority: int = Field(
        default=0,
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

    is_active: bool = Field(
        default=True,
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