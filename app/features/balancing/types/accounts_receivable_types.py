from enum import StrEnum
from dataclasses import dataclass, field
from decimal import Decimal

from app.shared.types import CompanyType

class AccountsReceivableStatus(StrEnum):
    PENDING = "pending"
    PARTIALLY_COLLECTED = "partially_collected"
    COLLECTED = "collected"
    CANCELLED = "cancelled"

@dataclass
class AccountsReceivableUpdate:

    brand: CompanyType | None = None
    entity_name: str | None = None
    location: str | None = None
    amount: Decimal | None = None
    status: AccountsReceivableStatus | None = None

    fields_set: set[str] = field(default_factory=set)

@dataclass(slots=True)
class AccountsReceivableAnalysisResponse:

    total_amount: Decimal

    pending_amount: Decimal

    partially_collected_amount: Decimal

    collected_amount: Decimal