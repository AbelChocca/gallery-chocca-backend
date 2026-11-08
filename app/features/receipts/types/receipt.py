from dataclasses import dataclass
from decimal import Decimal

from app.features.receipts.types.document import BillingDocumentType
from app.features.customer.customer_types import IdentityDocumentType

@dataclass
class ReceiptAttachmentDTO:
    filename: str
    content: bytes

@dataclass
class ReceiptCustomerDTO:
    document_type: IdentityDocumentType
    document_number: str


@dataclass
class ReceiptItemDTO:
    sku: str
    description: str
    quantity: Decimal

    # Precio FINAL unitario, incluyendo IGV
    unit_price: Decimal


@dataclass
class IssueReceiptDTO:
    receipt_type: BillingDocumentType  # "boleta" | "factura"
    customer: ReceiptCustomerDTO
    items: list[ReceiptItemDTO]
    currency: str = "PEN"


@dataclass
class IssuedReceiptDTO:
    external_id: str
    series_number: str

    status: str
    status_description: str

    accepted_by_sunat: bool

    sunat_code: str | None
    sunat_description: str | None

    environment: str | None
    has_fiscal_validity: bool

    remaining_credits: int | None