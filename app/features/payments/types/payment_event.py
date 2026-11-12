from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.features.payments.types.payment_provider import PaymentProvider

@dataclass
class PaymentEventDetailDTO:
    id: int
    provider: PaymentProvider
    event_type: str
    provider_event_id: str | None
    payload: dict[str, Any]
    created_at: datetime