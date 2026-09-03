from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, CheckConstraint
from sqlmodel import Field, SQLModel


class PromotionPricingRuleTable(SQLModel, table=True):
    __tablename__ = "promotion_pricing_rules"

    __table_args__ = (
            CheckConstraint(
    "execution_order >= 0",
    name="ck_promotion_pricing_rule_execution_order_positive",
),
        )

    promotion_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "promotions.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
            nullable=False,
        )
    )

    pricing_rule_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "pricing_rules.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
            nullable=False,
        )
    )

    execution_order: int = Field(
        default=0,
        nullable=False,
    )

    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )