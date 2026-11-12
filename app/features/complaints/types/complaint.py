from enum import Enum
from datetime import datetime
from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal


class ComplaintType(str, Enum):
    RECLAMO = "RECLAMO"
    QUEJA = "QUEJA"


class ComplaintGoodType(str, Enum):
    PRODUCTO = "PRODUCTO"
    SERVICIO = "SERVICIO"


class ComplaintDocumentType(str, Enum):
    DNI = "DNI"
    CE = "CE"
    PASAPORTE = "PASAPORTE"


class ComplaintResponseChannel(str, Enum):
    EMAIL = "EMAIL"
    CARTA = "CARTA"


class ComplaintStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    RESPONDED = "RESPONDED"

@dataclass(frozen=True, slots=True)
class ComplaintProviderIdentity:
    legal_name: str
    ruc: str
    address: str

@dataclass(frozen=True, slots=True)
class CreateComplaintInput:
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


@dataclass(frozen=True, slots=True)
class CreateComplaintResult:
    public_id: UUID
    complaint_number: str
    status: ComplaintStatus
    created_at: datetime
    receipt_email_sent: bool

@dataclass(frozen=True, slots=True)
class AdminComplaintListItemDTO:
    id: int
    complaint_number: str
    customer_name: str
    complaint_type: ComplaintType
    status: ComplaintStatus
    response_channel: ComplaintResponseChannel
    created_at: datetime
    response_due_at: datetime | None
    responded_at: datetime | None


@dataclass(frozen=True, slots=True)
class ComplaintFilters:
    search: str | None = None
    status: ComplaintStatus | None = None
    complaint_type: ComplaintType | None = None
    created_at_from: datetime | None = None
    created_at_to: datetime | None = None