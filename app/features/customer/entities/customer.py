from dataclasses import dataclass
from datetime import datetime

from app.features.customer.customer_types import (
    IdentityDocumentType,
    CustomerType,
)


@dataclass
class CustomerEntity:
    id: int | None

    user_id: int | None
    session_id: str | None

    name: str
    last_name: str

    customer_type: CustomerType

    document_type: IdentityDocumentType | None = None
    document_number: str | None = None

    email: str | None = None
    phone: str | None = None
    address: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None