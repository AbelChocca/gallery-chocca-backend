from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, Column, ForeignKey, func
from sqlmodel import Field, SQLModel

from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
    InventoryValuationSubcategory,
)
from app.shared.types import CompanyType


class InventoryValuationTable(SQLModel, table=True):
    __tablename__ = "inventory_valuations"

    id: int | None = Field(default=None, primary_key=True)

    balance_snapshot_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "balance_snapshots.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    category: InventoryValuationCategory = Field(
        sa_type=SAEnum(
            InventoryValuationCategory,
            name="inventory_valuation_category",
        ),
        nullable=False,
    )

    subcategory: InventoryValuationSubcategory | None = Field(
        default=None,
        sa_type=SAEnum(
            InventoryValuationSubcategory,
            name="inventory_valuation_subcategory",
        ),
    )

    description: str = Field(
        max_length=255,
        nullable=False,
    )

    brand: CompanyType = Field(
        sa_column=Column(
            SAEnum(
                CompanyType,
                name="company_type"
            ),
            nullable=False
        )
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    quantity: Decimal = Field(
        max_digits=14,
        decimal_places=3,
        nullable=False,
    )

    unit_value: Decimal = Field(
        max_digits=14,
        decimal_places=2,
        nullable=False,
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )