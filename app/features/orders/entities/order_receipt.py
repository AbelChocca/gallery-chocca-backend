from dataclasses import dataclass
from datetime import datetime

from app.features.orders.types.order_receipt import ReceiptStatus


@dataclass
class OrderReceipt:
    order_id: int
    status: ReceiptStatus

    id: int | None = None

    external_id: str | None = None
    series_number: str | None = None

    provider_error_code: str | None = None
    provider_error_message: str | None = None

    issued_at: datetime | None = None

    email_provider_id: str | None = None
    email_sent_at: datetime | None = None
    email_error_message: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def is_issued(self) -> bool:
        return self.status == ReceiptStatus.ISSUED