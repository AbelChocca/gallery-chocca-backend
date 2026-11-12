
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SQLEnum,
    Sequence,
    Text,
)
from sqlmodel import Field, SQLModel

from app.features.complaints.types.complaint import (
    ComplaintType,
    ComplaintGoodType,
    ComplaintDocumentType,
    ComplaintResponseChannel,
    ComplaintStatus,
)


complaint_number_sequence = Sequence(
    "complaint_number_seq",
    start=1,
    increment=1,
)


def enum_column(enum_type, name: str):
    return SQLEnum(
        enum_type,
        values_callable=lambda enum: [e.value for e in enum],
        native_enum=False,
        create_constraint=True,
        name=name,
    )


class ComplaintTable(SQLModel, table=True):
    __tablename__ = "complaints"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    public_id: UUID = Field(
        default_factory=uuid4,
        unique=True,
        index=True,
        nullable=False,
    )

    complaint_number: str = Field(
        max_length=30,
        unique=True,
        index=True,
        nullable=False,
    )

    # Snapshot del proveedor
    provider_legal_name: str = Field(max_length=255)
    provider_ruc: str = Field(max_length=11)

    provider_address: str = Field(
        sa_column=Column(Text, nullable=False),
    )

    # Consumidor
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=150)

    document_type: ComplaintDocumentType = Field(
        sa_column=Column(
            enum_column(
                ComplaintDocumentType,
                "ck_complaints_document_type",
            ),
            nullable=False,
        ),
    )

    document_number: str = Field(max_length=20)

    email: str | None = Field(
        default=None,
        max_length=320,
    )

    phone: str | None = Field(
        default=None,
        max_length=25,
    )

    address: str = Field(
        sa_column=Column(Text, nullable=False),
    )

    is_minor: bool = Field(default=False)

    representative_name: str | None = Field(
        default=None,
        max_length=250,
    )

    representative_document: str | None = Field(
        default=None,
        max_length=20,
    )

    # Bien contratado
    good_type: ComplaintGoodType = Field(
        sa_column=Column(
            enum_column(
                ComplaintGoodType,
                "ck_complaints_good_type",
            ),
            nullable=False,
        ),
    )

    order_number: str | None = Field(
        default=None,
        max_length=50,
        index=True,
    )

    amount: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
    )

    product_description: str = Field(
        sa_column=Column(Text, nullable=False),
    )

    # Reclamo o queja
    complaint_type: ComplaintType = Field(
        sa_column=Column(
            enum_column(
                ComplaintType,
                "ck_complaints_type",
            ),
            nullable=False,
        ),
    )

    detail: str = Field(
        sa_column=Column(Text, nullable=False),
    )

    requested_solution: str = Field(
        sa_column=Column(Text, nullable=False),
    )

    response_channel: ComplaintResponseChannel = Field(
        sa_column=Column(
            enum_column(
                ComplaintResponseChannel,
                "ck_complaints_response_channel",
            ),
            nullable=False,
        ),
    )

    # Gestión administrativa
    status: ComplaintStatus = Field(
        default=ComplaintStatus.SUBMITTED,
        sa_column=Column(
            enum_column(
                ComplaintStatus,
                "ck_complaints_status",
            ),
            nullable=False,
            server_default=ComplaintStatus.SUBMITTED.value,
        ),
    )

    assigned_to_user_id: int | None = Field(
        default=None,
        foreign_key="usertable.id",  # Ajustar al nombre real
        index=True,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    response_due_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )

    responded_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
