from enum import StrEnum
from dataclasses import dataclass, field
from decimal import Decimal

class OtherCurrentLiabilityCategory(StrEnum):
    TAX = "tax"
    ESSALUD = "essalud"
    AFP = "afp"
    PAYROLL = "payroll"
    OTHER = "other"


class OtherCurrentLiabilityStatus(StrEnum):
    PENDING = "pending"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    CANCELLED = "cancelled"

@dataclass
class OtherCurrentLiabilityUpdate:

    category: OtherCurrentLiabilityCategory | None = None
    description: str | None = None
    amount: Decimal | None = None
    status: OtherCurrentLiabilityStatus | None = None

    fields_set: set[str] = field(default_factory=set)

@dataclass(slots=True)
class OtherCurrentLiabilitiesAnalysisResponse:

    total_amount: Decimal

    pending_amount: Decimal

    partially_paid_amount: Decimal

    paid_amount: Decimal