from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.features.pricing.types.pricing_rules_types import PricingRuleType


class PricingRuleTable(SQLModel, table=True):
    __tablename__ = "pricing_rules"

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
        sa_column=Column(Text, nullable=True),
    )

    type: PricingRuleType = Field(
        nullable=False,
    )

    parameters: dict = Field(
        sa_column=Column(
            JSONB,
            nullable=False,
        )
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