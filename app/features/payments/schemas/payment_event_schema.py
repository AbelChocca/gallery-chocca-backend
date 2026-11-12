from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.features.payments.types.payment_provider import PaymentProvider



class PaymentEventDetailResponseSchema(
    BaseModel
):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    provider: PaymentProvider
    event_type: str
    provider_event_id: str | None
    payload: dict[str, Any]
    created_at: datetime