from app.features.sales.types.sale_document import ElectronicInvoiceProvider, SaleDocumentStatus, SaleDocumentType, CurrencyType, SunatTransactionType

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel


class SaleDocument(SQLModel, table=True):
    __tablename__ = "sale_document"

    id: int | None = Field(default=None, primary_key=True)

    sale_id: int = Field(
        foreign_key="sale.id",
        nullable=False,
    )

    provider: ElectronicInvoiceProvider = Field(
        sa_column=Column(
            ENUM(
                ElectronicInvoiceProvider,
                name="electronic_invoice_provider",
                create_type=False,
            ),
            nullable=False,
        )
    )

    document_type: SaleDocumentType = Field(
        sa_column=Column(
            ENUM(
                SaleDocumentType,
                name="sale_document_type",
                create_type=False,
            ),
            nullable=False,
        )
    )

    currency: CurrencyType = Field(
        default=CurrencyType.PEN,
        sa_column=Column(
            ENUM(
                CurrencyType,
                name="currency_type",
                create_type=False,
            ),
            nullable=False,
        )
    )

    sunat_transaction: SunatTransactionType = Field(
        sa_column=Column(
            ENUM(
                SunatTransactionType,
                name="sunat_transaction_type",
                create_type=False,
            ),
            nullable=False,
        )
    )

    sunat_status: SaleDocumentStatus = Field(
        default=SaleDocumentStatus.PENDING,
        sa_column=Column(
            ENUM(
                SaleDocumentStatus,
                name="sale_document_status",
                create_type=False,
            ),
            nullable=False,
        )
    )

    series: str = Field(max_length=4)

    number: int

    external_url: str | None = Field(default=None, max_length=500)

    pdf_url: str | None = Field(default=None, max_length=500)

    xml_url: str | None = Field(default=None, max_length=500)

    cdr_url: str | None = Field(default=None, max_length=500)

    qr_text: str | None = Field(default=None)

    hash: str | None = Field(default=None, max_length=255)

    sunat_response_code: str | None = Field(default=None, max_length=20)

    sunat_description: str | None = Field(default=None)

    sunat_note: str | None = Field(default=None)

    sunat_soap_error: str | None = Field(default=None)

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )