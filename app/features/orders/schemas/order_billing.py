from pydantic import BaseModel, ConfigDict

from app.features.customer.customer_types import (
    IdentityDocumentType,
)
from app.features.receipts.types.document import (
    BillingDocumentType,
)

class AdminOrderBillingResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    document_type: BillingDocumentType

    identity_document_type: IdentityDocumentType
    identity_document_number: str

    recipient_name: str
    email: str

    billing_address: str | None

class MyOrderBillingResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    document_type: BillingDocumentType

    identity_document_type: IdentityDocumentType

    identity_document_number: str

    recipient_name: str

    email: str

    billing_address: str | None