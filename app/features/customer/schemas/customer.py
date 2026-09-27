from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.features.sales.types.customer import (
    CustomerDocumentType,
    CustomerType,
)


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
        CustomerDocumentType | None
    )

    document_number: str | None

    email: str | None
    phone: str | None

class CustomerFiltersSchema(BaseModel):
    search: str | None = None
    customer_type: CustomerType | None = None
    document_type: CustomerDocumentType | None = None


class CustomerResponseSchema(BaseModel):
    model_config = ConfigDict(
            from_attributes=True
        )
    
    id: int
    name: str
    customer_type: CustomerType
    document_type: CustomerDocumentType | None
    document_number: str | None
    email: str | None
    phone: str | None