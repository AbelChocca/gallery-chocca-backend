from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SQLEnum
from app.features.receipts.types.document import BillingDocumentType
from app.features.customer.customer_types import IdentityDocumentType

class OrderBillingTable(SQLModel, table=True):
    __tablename__ = "order_billings"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    order_id: int = Field(
        foreign_key="orders.id",
        nullable=False,
        unique=True,
        index=True,
    )

    document_type: BillingDocumentType = Field(
        sa_column=Column(
            SQLEnum(
                BillingDocumentType,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="ck_order_billings_document_type",
            ),
            nullable=False,
        ),
    )

    identity_document_type: IdentityDocumentType = Field(
        sa_column=Column(
            SQLEnum(
                IdentityDocumentType,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="ck_order_billings_document_number_type",
            ),
            nullable=False,
        ),
    )

    identity_document_number: str = Field(
        max_length=11,
        nullable=False,
    )

    recipient_name: str = Field(
        max_length=200,
        nullable=False,
    )

    email: str = Field(
        max_length=255,
        nullable=False,
    )

    billing_address: str | None = Field(
        default=None,
        max_length=255,
    )