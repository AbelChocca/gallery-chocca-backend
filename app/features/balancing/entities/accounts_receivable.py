from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableStatus,
)
from app.shared.types import CompanyType

@dataclass
class AccountsReceivable:
    balance_snapshot_id: int
    brand: CompanyType
    entity_name: str
    location: str | None
    amount: Decimal
    status: AccountsReceivableStatus
    id: int | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None