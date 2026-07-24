from app.features.inventory.types.inventory_location import InventoryLocationType

from datetime import datetime, timezone

from sqlalchemy import Index, Column, DateTime
from sqlmodel import Field, SQLModel


class InventoryLocationTable(SQLModel, table=True):
    __tablename__ = "inventory_location"

    __table_args__ = (
        Index("ix_inventory_location_name", "name"),
    )

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    type: InventoryLocationType

    address: str | None = Field(default=None, max_length=255)

    is_active: bool = Field(default=True)

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True)
        )
    )