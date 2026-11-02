from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class ReceiptStatus(str, Enum):
    PENDING = "PENDING"
    ISSUING = "ISSUING"
    ISSUED = "ISSUED"
    RETRY_PENDING = "RETRY_PENDING"
    FAILED = "FAILED"

class ReceiptEmailStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

@dataclass
class AdminOrderReceiptDTO:
    status: ReceiptStatus

    external_id: str | None
    series_number: str | None

    provider_error_code: str | None
    provider_error_message: str | None

    issued_at: datetime | None

    email_provider_id: str | None
    email_sent_at: datetime | None
    email_error_message: str | None