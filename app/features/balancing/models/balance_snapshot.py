from datetime import date, datetime

from sqlalchemy import CheckConstraint, DateTime, Enum as SAEnum, Column, func
from sqlmodel import Field, SQLModel

from app.features.balancing.types.balance_snapshot_types import (
    BalanceSnapshotStatus,
)


class BalanceSnapshotTable(SQLModel, table=True):
    __tablename__ = "balance_snapshots"

    id: int | None = Field(default=None, primary_key=True)

    period_start: date = Field(nullable=False)

    period_end: date = Field(nullable=False)

    status: BalanceSnapshotStatus = Field(
        sa_type=SAEnum(BalanceSnapshotStatus, name="balance_snapshot_status"),
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
            nullable=False
        )
    )

    __table_args__ = (
        CheckConstraint(
            "period_start <= period_end",
            name="ck_balance_snapshots_period_valid",
        ),
    )