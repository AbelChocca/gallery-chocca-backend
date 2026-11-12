from dataclasses import dataclass

from app.features.customer.customer_types import (
    IdentityDocumentType,
    CustomerType,
)


@dataclass(frozen=True, slots=True)
class CustomerSearchOptionDTO:
    id: int
    name: str

    customer_type: CustomerType

    document_type: IdentityDocumentType | None
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
    document_type: IdentityDocumentType | None = None

@dataclass(frozen=True, slots=True)
class AdminOrderCustomerDTO:
    id: int

    name: str
    last_name: str

    document_type: IdentityDocumentType | None
    document_number: str | None

    email: str | None
    phone: str | None

@dataclass(frozen=True, slots=True)
class MyOrderCustomerDTO:
    name: str
    last_name: str
    email: str | None
    phone: str | None