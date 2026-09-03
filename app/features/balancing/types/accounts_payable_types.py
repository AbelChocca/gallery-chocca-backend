from enum import StrEnum
from dataclasses import dataclass, field
from decimal import Decimal

class AccountsPayableStatus(StrEnum):
    PENDING = "pending"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    CANCELLED = "cancelled"


class AccountsPayableCostCenter(StrEnum):
    FABRIC = "fabric"
    SEWING = "sewing"
    LAUNDRY = "laundry"

@dataclass
class AccountsPayableUpdate:

    brand: str | None = None
    entity_name: str | None = None
    cost_center: AccountsPayableCostCenter | None = None
    amount: Decimal | None = None
    status: AccountsPayableStatus | None = None

    fields_set: set[str] = field(default_factory=set)

@dataclass(slots=True)
class AccountsPayableAnalysisResponse:

    total_amount: Decimal

    pending_amount: Decimal

    partially_paid_amount: Decimal

    paid_amount: Decimal