from dataclasses import dataclass

from app.features.receipts.types.document import BillingDocumentType
from app.features.customer.customer_types import IdentityDocumentType

@dataclass(frozen=True, slots=True)
class AdminOrderBillingDTO:
    document_type: BillingDocumentType

    identity_document_type: IdentityDocumentType
    identity_document_number: str

    recipient_name: str

    email: str

    billing_address: str | None

@dataclass(frozen=True, slots=True)
class MyOrderBillingDTO:
    document_type: BillingDocumentType

    identity_document_type: IdentityDocumentType

    identity_document_number: str

    recipient_name: str

    email: str

    billing_address: str | None