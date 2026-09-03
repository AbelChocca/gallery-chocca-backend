from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.balancing.types.other_current_liability_types import (
    OtherCurrentLiabilityCategory,
    OtherCurrentLiabilityStatus,
)


@dataclass
class OtherCurrentLiability:
    balance_snapshot_id: int
    category: OtherCurrentLiabilityCategory
    description: str
    amount: Decimal
    status: OtherCurrentLiabilityStatus

    id: int | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None
    