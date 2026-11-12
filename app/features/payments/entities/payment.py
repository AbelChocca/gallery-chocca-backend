from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.payments.types.payment import PaymentProvider, PaymentStatus, PaymentMethod


@dataclass(slots=True)
class Payment:
    id: int | None

    order_id: int

    provider: PaymentProvider
    payment_method: PaymentMethod 
    status: PaymentStatus

    amount: Decimal
    currency: str

    provider_payment_id: str | None
    provider_order_id: str

    checkout_id: str | None
    payment_link: str | None
    expires_at: datetime | None

    authorization: str | None

    error_code: str | None
    error_message: str | None

    created_at: datetime
    updated_at: datetime