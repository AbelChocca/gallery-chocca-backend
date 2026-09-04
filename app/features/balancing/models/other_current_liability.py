from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, Column, func
from sqlmodel import Field, SQLModel

from app.features.balancing.types.other_current_liability_types import (
    OtherCurrentLiabilityCategory,
    OtherCurrentLiabilityStatus,
)


class OtherCurrentLiabilityTable(SQLModel, table=True):
    __tablename__ = "other_current_liabilities"

    id: int | None = Field(default=None, primary_key=True)

    balance_snapshot_id: int = Field(
        foreign_key="balance_snapshots.id",
        nullable=False,
        index=True,
    )

    category: OtherCurrentLiabilityCategory = Field(
        sa_type=SAEnum(
            OtherCurrentLiabilityCategory,
            name="other_current_liability_category",
        ),
        nullable=False,
    )

    description: str = Field(
        max_length=255,
        nullable=False,
    )

    amount: Decimal = Field(
        max_digits=14,
        decimal_places=2,
        nullable=False,
    )

    status: OtherCurrentLiabilityStatus = Field(
        sa_type=SAEnum(
            OtherCurrentLiabilityStatus,
            name="other_current_liability_status",
        ),
        nullable=False,
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )