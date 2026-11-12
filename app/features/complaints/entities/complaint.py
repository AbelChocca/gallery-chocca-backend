
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.features.complaints.types.complaint import (
    ComplaintType,
    ComplaintGoodType,
    ComplaintDocumentType,
    ComplaintResponseChannel,
    ComplaintStatus,
)


@dataclass
class Complaint:
    complaint_number: str
    public_id: UUID

    provider_legal_name: str
    provider_ruc: str
    provider_address: str

    first_name: str
    last_name: str
    document_type: ComplaintDocumentType
    document_number: str
    email: str | None
    phone: str | None
    address: str

    is_minor: bool
    representative_name: str | None
    representative_document: str | None

    good_type: ComplaintGoodType
    order_number: str | None
    amount: Decimal | None
    product_description: str

    complaint_type: ComplaintType
    detail: str
    requested_solution: str

    response_channel: ComplaintResponseChannel
    status: ComplaintStatus

    id: int | None = None
    assigned_to_user_id: int | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    response_due_at: datetime | None = None
    responded_at: datetime | None = None

    @staticmethod
    def generate_complaint_number(
        sequence: int,
        created_at: datetime,
    ) -> str:
        return f"LR-{created_at.year}-{sequence:06d}"
