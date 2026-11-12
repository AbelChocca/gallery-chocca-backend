from dataclasses import dataclass

from app.features.receipts.types.document import (
    BillingDocumentType,
)
from app.features.customer.customer_types import IdentityDocumentType

@dataclass
class OrderBilling:
    order_id: int

    document_type: BillingDocumentType
    identity_document_type: IdentityDocumentType
    identity_document_number: str

    recipient_name: str
    email: str

    id: int | None = None

    billing_address: str | None = None