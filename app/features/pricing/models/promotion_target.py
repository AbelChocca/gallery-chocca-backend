from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint
)
from sqlmodel import Field, SQLModel

from app.features.pricing.types.promotion_types import PromotionTargetType


class PromotionTargetTable(SQLModel, table=True):
    __tablename__ = "promotion_targets"

    __table_args__ = (
        CheckConstraint(
    """
    (
        target_type = 'ALL'
        AND reference_id IS NULL
        AND reference_value IS NULL
    )
    OR
    (
        target_type = 'PRODUCT'
        AND reference_id IS NOT NULL
        AND reference_value IS NULL
    )
    OR
    (
        target_type IN ('CATEGORY', 'BRAND', 'COLLECTION')
        AND reference_id IS NULL
        AND reference_value IS NOT NULL
    )
    """,
    name="ck_promotion_target_reference",
),
        UniqueConstraint(
    "promotion_id",
    "target_type",
    "reference_id",
    "reference_value",
    name="uq_promotion_target",
)
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

    target_type: PromotionTargetType = Field(
        nullable=False,
        index=True,
    )

    reference_id: int | None = Field(
        default=None,
        nullable=True,
        index=True,
    )

    reference_value: str | None = Field(
        default=None,
        max_length=255,
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