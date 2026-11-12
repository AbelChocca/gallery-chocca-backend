
from dataclasses import dataclass
from datetime import datetime

from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)


@dataclass
class ComplaintResponse:
    complaint_id: int
    message: str
    status: ComplaintResponseStatus

    author_user_id: int | None = None
    recipient_email: str | None = None

    external_message_id: str | None = None
    error_message: str | None = None
    physical_delivery_reference: str | None = None

    id: int | None = None

    created_at: datetime | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
