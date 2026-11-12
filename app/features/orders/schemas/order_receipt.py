from datetime import datetime

from pydantic import BaseModel, ConfigDict
from app.features.orders.types.order_receipt import ReceiptStatus

class AdminOrderReceiptResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    status: ReceiptStatus

    external_id: str | None
    series_number: str | None

    provider_error_code: str | None
    provider_error_message: str | None

    issued_at: datetime | None

    email_provider_id: str | None
    email_sent_at: datetime | None
    email_error_message: str | None