from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, DateTime, Enum as SQLEnum
from sqlmodel import Field, SQLModel

from app.features.locations.types import LocationType

class LocationTable(SQLModel, table=True):
    __tablename__ = "locations"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=150,
        nullable=False,
        index=True,
    )

    type: LocationType = Field(
        sa_column=Column(
            SQLEnum(
                LocationType,
                values_callable=lambda enum: [
                    e.value for e in enum
                ],
                native_enum=False,
                create_constraint=True,
                name="ck_locations_type",
            ),
            nullable=False,
        ),
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    ubigeo_code: str | None = Field(
        default=None,
        foreign_key="ubigeos.code",
        max_length=6,
        index=True,
    )

    latitude: Decimal | None = Field(
        default=None,
        max_digits=9,
        decimal_places=6,
    )

    longitude: Decimal | None = Field(
        default=None,
        max_digits=9,
        decimal_places=6,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    reference: str | None = Field(
        default=None,
        max_length=255,
    )

    external_provider: str | None = Field(
        default=None,
        max_length=50,
        index=True,
    )

    external_code: str | None = Field(
        default=None,
        max_length=100,
        index=True,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
        index=True,
    )

    pickup_enabled: bool = Field(
        default=False,
        nullable=False,
        index=True,
    )

    created_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )