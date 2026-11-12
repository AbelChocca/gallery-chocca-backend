from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OpenpayWebhookTransactionSchema(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    id: str

    authorization: str | None = None

    status: str | None = None

    order_id: str | None = None

    amount: Decimal | None = None

    currency: str | None = None

    error_message: str | None = None


class OpenpayWebhookSchema(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    type: str

    event_date: datetime | None = None

    transaction: OpenpayWebhookTransactionSchema | None = None

    verification_code: str | None = None