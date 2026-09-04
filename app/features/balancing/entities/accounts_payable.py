from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.balancing.types.accounts_payable_types import (
    AccountsPayableCostCenter,
    AccountsPayableStatus,
)


@dataclass
class AccountsPayable:
    balance_snapshot_id: int
    brand: str
    entity_name: str
    cost_center: AccountsPayableCostCenter | None
    amount: Decimal
    status: AccountsPayableStatus
    id: int | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None