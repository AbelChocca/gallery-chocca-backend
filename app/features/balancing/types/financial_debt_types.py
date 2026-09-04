from enum import StrEnum
from dataclasses import dataclass, field
from decimal import Decimal

class FinancialDebtStatus(StrEnum):
    ACTIVE = "active"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    CANCELLED = "cancelled"

@dataclass
class FinancialDebtUpdate:

    bank_name: str | None = None
    amount: Decimal | None = None
    status: FinancialDebtStatus | None = None

    fields_set: set[str] = field(default_factory=set)
    
@dataclass(slots=True)
class FinancialDebtAnalysisResponse:

    total_amount: Decimal

    active_amount: Decimal

    partially_paid_amount: Decimal

    paid_amount: Decimal