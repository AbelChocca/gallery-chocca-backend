from dataclasses import dataclass
from datetime import date, datetime

from app.features.balancing.types.balance_snapshot_types import (
    BalanceSnapshotStatus,
)


@dataclass
class BalanceSnapshot:
    period_start: date
    period_end: date
    status: BalanceSnapshotStatus
    id: int | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    