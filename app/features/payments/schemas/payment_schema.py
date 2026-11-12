from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.features.payments.types.payment import (
    PaymentStatus,
    PaymentMethod,
)
from app.features.payments.types.payment_provider import PaymentProvider


from app.features.payments.schemas.payment_event_schema import PaymentEventDetailResponseSchema


class CreatePaymentCheckoutRequestSchema(
    BaseModel
):
    send_email: bool = False

    expiration_date: datetime | None = Field(
        default=None,
        description=(
            "Fecha de expiración del link de pago."
        ),
    )


class CreatePaymentCheckoutResponseSchema(
    BaseModel
):
    model_config = ConfigDict(
        from_attributes=True,
    )

    payment_id: int

    status: PaymentStatus

    amount: Decimal
    currency: str

    checkout_id: str
    checkout_link: str

    expires_at: datetime | None


class CreateCardChargeRequestSchema(
    BaseModel
):
    model_config = ConfigDict(
        extra="forbid"
    )

    token_id: str = Field(
        min_length=1,
        max_length=100,
    )

    device_session_id: str = Field(
        min_length=1,
        max_length=100,
    )


class CreateCardChargeResponseSchema(
    BaseModel
):
    model_config = ConfigDict(
        from_attributes=True,
    )

    payment_id: int
    order_id: int
    status: str
    redirect_url: str | None

class PaymentDetailResponseSchema(
    BaseModel
):
    model_config = ConfigDict(
        from_attributes=True,
    )

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

    events: list[
        PaymentEventDetailResponseSchema
    ]