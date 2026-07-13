from sqlmodel import SQLModel, Field, Column, ForeignKey, Numeric, Relationship, UniqueConstraint, CheckConstraint, Index
from decimal import Decimal
from sqlalchemy import String, Enum as SQLEnum, DateTime
from app.features.material.types import (
    CompanyType, 
    MaterialType, 
    UnitType,
    FiberType
)

from datetime import datetime, timezone


class MaterialTable(SQLModel, table=True):
    __tablename__ = "materials"
    __table_args__ = (
        Index(
            "ix_material_company_type_active",
            "company",
            "material_type",
            "is_active"
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    code: str = Field(
        max_length=20,
        sa_column=Column(
            String(20),
            nullable=False,
            unique=True
        )
    )

    name: str = Field(
        min_length=3,
        max_length=100,
        sa_column=Column(
            String(100),
            nullable=False,
            index=True
        )
    )

    description: str | None = Field(
        default=None,
        max_length=255,
        sa_column=Column(
            String(255),
            nullable=True
        )
    )

    material_type: MaterialType = Field(
        sa_column=Column(
            SQLEnum(
                MaterialType,
                name="material_type"
            ),
            nullable=False
        )
    )

    unit_type: UnitType = Field(
        sa_column=Column(
            SQLEnum(
                UnitType,
                name="unit_type"
            ),
            nullable=False
        )
    )

    company: CompanyType = Field(
        sa_column=Column(
            SQLEnum(
                CompanyType,
                name="company_type"
            ),
            nullable=False
        )
    )

    stock: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
            default=0
        )
    )

    minimum_stock: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
            default=0
        )
    )

    is_active: bool = Field(
        default=True
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )

    components: list["MaterialComponentTable"] = Relationship(
        back_populates="material",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )

class MaterialComponentTable(SQLModel, table=True):
    __tablename__ = "material_components"
    __table_args__ = (
        UniqueConstraint(
            "material_id",
            "fiber_type",
            name="uq_material_component_material_fiber"
        ),
        CheckConstraint(
            "percentage BETWEEN 0.01 AND 100",
            name="ck_material_component_percentage_range"
        )
    )

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    material_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "materials.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True
        )
    )

    fiber_type: FiberType = Field(
        sa_column=Column(
            SQLEnum(
                FiberType,
                name="fiber_type"
            ),
            nullable=False
        )
    )

    percentage: Decimal = Field(
        sa_column=Column(
            Numeric(5, 2),
            nullable=False
        )
    )

    material: "MaterialTable" = Relationship(
        back_populates="components",
        sa_relationship_kwargs={
            "lazy": "selectin"
        }
    )