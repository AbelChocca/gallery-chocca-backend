from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum

class ChargeStatus(str, Enum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

class CheckoutStatus(str, Enum):
    AVAILABLE = "AVAILABLE"

class PaymentProvider(str, Enum):
    OPENPAY = "OPENPAY"
    MANUAL = "MANUAL"
    CULQI = "CULQI"

@dataclass(frozen=True, slots=True)
class CheckoutCustomer:
    name: str
    last_name: str
    email: str
    phone_number: str


@dataclass(frozen=True, slots=True)
class CreateCheckoutRequest:
    amount: Decimal
    currency: str

    description: str
    order_id: str

    redirect_url: str

    customer: CheckoutCustomer

    send_email: bool = False
    expiration_date: datetime | None = None


@dataclass(frozen=True, slots=True)
class CheckoutResult:
    provider_checkout_id: str

    status: CheckoutStatus

    checkout_link: str

    creation_date: datetime

    expiration_date: datetime | None

@dataclass(frozen=True, slots=True)
class CardChargeCustomer:
    name: str
    last_name: str
    email: str
    phone_number: str


@dataclass(frozen=True, slots=True)
class CreateCardChargeRequest:
    token_id: str
    device_session_id: str

    amount: Decimal
    currency: str

    description: str
    order_id: str

    customer: CardChargeCustomer

    client_ip: str

    use_3d_secure: bool = False
    redirect_url: str | None = None


@dataclass(frozen=True, slots=True)
class CardChargeResult:
    provider_payment_id: str

    status: str

    authorization: str | None

    error_message: str | None

    redirect_url: str | None