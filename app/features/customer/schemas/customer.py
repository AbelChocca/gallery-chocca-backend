from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.features.customer.customer_types import (
    IdentityDocumentType,
    CustomerType,
)

class AdminOrderCustomerResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    name: str
    last_name: str

    document_type: IdentityDocumentType | None
    document_number: str | None

    email: str | None
    phone: str | None

class CustomerSearchOptionResponseSchema(
    BaseModel
):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str

    customer_type: CustomerType

    document_type: (
        IdentityDocumentType | None
    )

    document_number: str | None

    email: str | None
    phone: str | None

class CustomerFiltersSchema(BaseModel):
    search: str | None = None
    customer_type: CustomerType | None = None
    document_type: IdentityDocumentType | None = None


class CustomerResponseSchema(BaseModel):
    model_config = ConfigDict(
            from_attributes=True
        )
    
    id: int
    name: str
    customer_type: CustomerType
    document_type: IdentityDocumentType | None
    document_number: str | None
    email: str | None
    phone: str | None

class MyOrderCustomerResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: str
    last_name: str

    email: str | None
    phone: str | None
