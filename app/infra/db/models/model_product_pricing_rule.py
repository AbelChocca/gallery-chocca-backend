from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey
from sqlmodel import SQLModel, Field

class ProductPricingRuleTable(SQLModel, table=True):
    __tablename__ = "product_pricing_rules"

    product_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "product.id",
                ondelete="CASCADE"
            ),
            primary_key=True,
            nullable=False
        )
    )

    pricing_rule_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "pricing_rules.id",
                ondelete="CASCADE"
            ),
            primary_key=True,
            nullable=False
        )
    )

    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )