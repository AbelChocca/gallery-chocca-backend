# app/features/payments/entities/payment_event.py

from dataclasses import dataclass
from datetime import datetime

from app.features.payments.types.payment import PaymentProvider


@dataclass(slots=True)
class PaymentEvent:
    id: int | None

    payment_id: int | None

    provider: PaymentProvider

    event_type: str

    provider_event_id: str | None

    payload: dict

    created_at: datetime