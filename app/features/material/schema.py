from pydantic import BaseModel, Field
from fastapi import Form
from datetime import datetime

from app.features.media.schema import ReadImage
from app.shared.pagination.schema import PaginatedResponseSchema
from app.features.material.types import CompanyType, MaterialAvailabilityStatus, UnitType, MaterialType

class GetMaterialsQuerySchema(BaseModel):
    search: str | None = None

    company: CompanyType | None = None

    material_type: MaterialType | None = None

    is_active: bool | None = None

    availability_status: (
        MaterialAvailabilityStatus | None
    ) = None

class MaterialResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None

    company: CompanyType
    material_type: MaterialType
    unit_type: UnitType

    stock: int
    minimum_stock: int

    is_active: bool

    availability_status: MaterialAvailabilityStatus

    image: ReadImage | None = None

    created_at: datetime
    updated_at: datetime

class MaterialCatalogResponseSchema(BaseModel):
    id: int
    code: str
    name: str

    material_type: MaterialType
    unit_type: UnitType

    stock: int
    minimum_stock: int

    is_active: bool

    availability_status: MaterialAvailabilityStatus

    image: ReadImage | None = None

class MaterialPaginatedResponseSchema(
    PaginatedResponseSchema[MaterialCatalogResponseSchema]
):
    pass

# Material
class CreateSupplyRequest(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )

    company: CompanyType

    material_type: MaterialType

    unit_type: UnitType

    minimum_stock: int = Field(
        ge=0
    )

    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=3, max_length=100),
        description: str = Form(..., max_length=255),
        company: CompanyType = Form(...),
        material_type: MaterialType = Form(...),
        unit_type: UnitType = Form(...),
        minimum_stock: int = Form(..., ge=0)
    ):
        return cls(
            name=name,
            description=description,
            company=company,
            material_type=material_type,
            unit_type=unit_type,
            minimum_stock=minimum_stock
        )


class UpdateMaterialRequest(BaseModel):
    name: str | None = Field(
        None,
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )

    company: CompanyType | None = Field(None)

    material_type: MaterialType | None = Field(None)

    unit_type: UnitType | None = Field(None)

    minimum_stock: int | None = Field(
        None,
        ge=0
    )