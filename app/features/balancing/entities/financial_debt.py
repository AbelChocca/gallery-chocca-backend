from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.balancing.types.financial_debt_types import (
    FinancialDebtStatus,
)


@dataclass
class FinancialDebt:
    balance_snapshot_id: int
    bank_name: str
    amount: Decimal
    status: FinancialDebtStatus
    id: int | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    