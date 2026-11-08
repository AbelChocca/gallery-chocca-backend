from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)

from app.features.complaints.types.complaint import (
    ComplaintType,
    ComplaintGoodType,
    ComplaintDocumentType,
    ComplaintResponseChannel,
    ComplaintStatus,
)


class CreateComplaintRequestSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    # Consumidor
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=150)

    document_type: ComplaintDocumentType
    document_number: str = Field(min_length=5, max_length=20)

    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=25)

    address: str = Field(min_length=5, max_length=500)

    is_minor: bool = False

    representative_name: str | None = Field(
        default=None,
        max_length=250,
    )
    representative_document: str | None = Field(
        default=None,
        max_length=20,
    )

    # Producto / servicio
    good_type: ComplaintGoodType

    order_number: str | None = Field(
        default=None,
        max_length=50,
    )

    amount: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    product_description: str = Field(
        min_length=3,
        max_length=2000,
    )

    # Reclamo / queja
    complaint_type: ComplaintType

    detail: str = Field(
        min_length=10,
        max_length=10000,
    )

    requested_solution: str = Field(
        min_length=3,
        max_length=5000,
    )

    response_channel: ComplaintResponseChannel = (
        ComplaintResponseChannel.EMAIL
    )

    @model_validator(mode="after")
    def validate_business_rules(self):
        if self.document_type == ComplaintDocumentType.DNI:
            if (
                not self.document_number.isdigit()
                or len(self.document_number) != 8
            ):
                raise ValueError(
                    "El DNI debe contener 8 dígitos"
                )

        if self.is_minor:
            if (
                not self.representative_name
                or not self.representative_document
            ):
                raise ValueError(
                    "Se requieren datos del representante"
                )

        if (
            self.response_channel == ComplaintResponseChannel.EMAIL
            and self.email is None
        ):
            raise ValueError(
                "El correo es obligatorio para recibir "
                "una respuesta por email"
            )

        return self


class CreateComplaintResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: UUID
    complaint_number: str
    status: ComplaintStatus
    created_at: datetime
    receipt_email_sent: bool



class AdminComplaintDetailResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    public_id: UUID
    complaint_number: str

    provider_legal_name: str
    provider_ruc: str
    provider_address: str

    first_name: str
    last_name: str
    document_type: ComplaintDocumentType
    document_number: str
    email: str | None
    phone: str | None
    address: str

    is_minor: bool
    representative_name: str | None
    representative_document: str | None

    good_type: ComplaintGoodType
    order_number: str | None
    amount: Decimal | None
    product_description: str

    complaint_type: ComplaintType
    detail: str
    requested_solution: str

    response_channel: ComplaintResponseChannel
    status: ComplaintStatus
    assigned_to_user_id: int | None

    created_at: datetime
    updated_at: datetime
    response_due_at: datetime | None
    responded_at: datetime | None

class AdminComplaintFiltersSchema(BaseModel):
    search: str | None = None
    status: ComplaintStatus | None = None
    complaint_type: ComplaintType | None = None

    created_at_from: date | None = None
    created_at_to: date | None = None


class AdminComplaintListItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_number: str
    customer_name: str
    complaint_type: ComplaintType
    status: ComplaintStatus
    response_channel: ComplaintResponseChannel

    created_at: datetime
    response_due_at: datetime | None
    responded_at: datetime | None