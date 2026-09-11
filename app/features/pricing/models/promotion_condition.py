from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    Enum as ENUM
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.features.pricing.types.promotion_types import PromotionConditionType


class PromotionConditionTable(SQLModel, table=True):
    __tablename__ = "promotion_conditions"

    __table_args__ = (
        UniqueConstraint(
            "promotion_id",
            "condition_type",
            name="uq_promotion_condition",
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


    condition_type: PromotionConditionType = Field(
        default=PromotionConditionType.REGULAR,
        sa_column=Column(
            ENUM(
                PromotionConditionType,
                name="promotion_audience_type",
            ),
            nullable=False,
            index=True
        ),
    )

    parameters: dict = Field(
        sa_column=Column(
            JSONB,
            nullable=False,
        )
    )

    description: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )