from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlmodel import Field, SQLModel

from app.features.pricing.types.promotion_types import PromotionAudienceType


class PromotionAudienceTable(SQLModel, table=True):
    __tablename__ = "promotion_audiences"

    __table_args__ = (
        CheckConstraint(
            """
            CASE
                WHEN audience_type = 'ALL_CUSTOMERS' THEN
                    reference_id IS NULL
                    AND reference_value IS NULL
                ELSE
                    (
                        (reference_id IS NOT NULL OR reference_value IS NOT NULL)
                        AND NOT (
                            reference_id IS NOT NULL
                            AND reference_value IS NOT NULL
                        )
                    )
            END
            """,
            name="ck_promotion_audience_reference",
        ),
        UniqueConstraint(
            "promotion_id",
            "audience_type",
            "reference_id",
            "reference_value",
            name="uq_promotion_audience",
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

    audience_type: PromotionAudienceType = Field(
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