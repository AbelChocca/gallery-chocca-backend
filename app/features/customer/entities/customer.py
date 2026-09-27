from dataclasses import dataclass
from datetime import datetime

from app.features.sales.types.customer import (
    CustomerDocumentType,
    CustomerType,
)


@dataclass
class CustomerEntity:
    id: int | None

    name: str

    customer_type: CustomerType

    document_type: CustomerDocumentType | None = None
    document_number: str | None = None

    email: str | None = None
    phone: str | None = None
    address: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None