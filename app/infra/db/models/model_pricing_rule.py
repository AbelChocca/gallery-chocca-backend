from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, DateTime, Numeric, Text, CheckConstraint
from sqlmodel import SQLModel, Field

from app.features.pricing.types import PricingRuleType

class PricingRuleTable(SQLModel, table=True):
    __tablename__ = "pricing_rules"
    __table_args__ = (
        CheckConstraint("value >= 0", name="ck_pricing_rule_value_positive"),
        CheckConstraint("priority >= 0", name="ck_pricing_rule_priority_positive"),
        CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at > starts_at",
            name="ck_pricing_rule_valid_dates"
        ),

    )

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(
        index=True,
        nullable=False,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=True)
    )

    type: PricingRuleType = Field(
        nullable=False
    )

    value: Decimal = Field(
        sa_column=Column(
            Numeric(10, 2),
            nullable=False
        )
    )

    is_active: bool = Field(
        default=True,
        nullable=False
    )

    is_stackable: bool = Field(
        default=True,
        nullable=False
    )

    priority: int = Field(
        default=0,
        nullable=False
    )

    starts_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        )
    )

    ends_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        )
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )