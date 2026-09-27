from dataclasses import dataclass

from app.features.sales.types.customer import (
    CustomerDocumentType,
    CustomerType,
)


@dataclass(frozen=True, slots=True)
class CustomerSearchOptionDTO:
    id: int
    name: str

    customer_type: CustomerType

    document_type: CustomerDocumentType | None
    document_number: str | None

    email: str | None
    phone: str | None

@dataclass(frozen=True, slots=True)
class CustomerPricingContext:
    customer_id: int
    customer_type: CustomerType

@dataclass(slots=True)
class CustomerFilters:
    search: str | None = None
    customer_type: CustomerType | None = None
    document_type: CustomerDocumentType | None = None