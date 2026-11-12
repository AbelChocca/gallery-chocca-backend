from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.features.payments.types.payment_event import PaymentEventDetailDTO
from app.features.payments.types.payment_provider import PaymentProvider

class PaymentMethod(str, Enum):
    CARD = "CARD"
    YAPE = "YAPE"
    PLIN = "PLIN"
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

@dataclass(frozen=True, slots=True)
class CreatePaymentCheckoutInput:
    send_email: bool = False
    expiration_date: datetime | None = None

@dataclass(frozen=True, slots=True)
class CreatePaymentCheckoutResult:
    payment_id: int

    status: PaymentStatus

    amount: Decimal
    currency: str

    checkout_id: str
    checkout_link: str

    expires_at: datetime | None

@dataclass(frozen=True, slots=True)
class CreateCardChargeCommand:
    order_id: int
    token_id: str
    device_session_id: str
    client_ip: str

@dataclass(frozen=True, slots=True)
class CreateCardChargeResult:
    payment_id: int
    order_id: int
    status: str
    redirect_url: str | None


@dataclass
class PaymentDetailDTO:
    id: int
    order_id: int

    provider: PaymentProvider
    payment_method: PaymentMethod
    status: PaymentStatus

    amount: Decimal
    currency: str

    provider_order_id: str
    provider_payment_id: str | None

    checkout_id: str | None
    payment_link: str | None
    expires_at: datetime | None

    authorization: str | None

    error_code: str | None
    error_message: str | None

    created_at: datetime
    updated_at: datetime

    events: list[PaymentEventDetailDTO]