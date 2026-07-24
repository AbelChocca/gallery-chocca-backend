from app.features.inventory.types.stock_transfer import StockTransferStatus

from decimal import Decimal
from datetime import datetime

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

class StockTransferTable(SQLModel, table=True):
    __tablename__ = "stock_transfer"

    __table_args__ = (
        CheckConstraint(
            "from_location_id <> to_location_id",
            name="ck_stock_transfer_different_locations",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    from_location_id: int = Field(
        foreign_key="inventory_location.id"
    )

    to_location_id: int = Field(
        foreign_key="inventory_location.id"
    )

    status: StockTransferStatus = Field(
        default=StockTransferStatus.PENDING
    )

    created_by: int = Field(
        foreign_key="usertable.id"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    received_at: datetime | None = None

    items: list["StockTransferItemTable"] = Relationship(
        back_populates="transfer"
    )

class StockTransferItemTable(SQLModel, table=True):
    __tablename__ = "stock_transfer_item"

    __table_args__ = (
        UniqueConstraint(
            "transfer_id",
            "variant_size_id",
            name="uq_stock_transfer_item",
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_stock_transfer_item_quantity_positive",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    transfer_id: int = Field(
        foreign_key="stock_transfer.id"
    )

    variant_size_id: int = Field(
        foreign_key="variant_size.id"
    )

    quantity: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )

    transfer: "StockTransferTable" = Relationship(
        back_populates="items"
    )