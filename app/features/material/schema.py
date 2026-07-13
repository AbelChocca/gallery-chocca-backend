from pydantic import BaseModel, Field
from fastapi import Form
from datetime import datetime
from decimal import Decimal
import orjson

from app.shared.decimal import PositiveDecimal
from app.features.media.schema import ReadImage
from app.shared.pagination.schema import PaginatedResponseSchema
from app.features.material.types import CompanyType, MaterialAvailabilityStatus, UnitType, MaterialType, FiberType

class MaterialComponentSchema(BaseModel):
    id: int
    material_id: int
    fiber_type: FiberType
    percentage: PositiveDecimal

class CreateMaterialComponentSchema(BaseModel):
    fiber_type: FiberType
    percentage: PositiveDecimal

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

    stock: Decimal
    minimum_stock: PositiveDecimal

    is_active: bool

    availability_status: MaterialAvailabilityStatus

    image: ReadImage | None = None

    components: list[MaterialComponentSchema] = Field(
        default_factory=list
    )

    created_at: datetime
    updated_at: datetime

class MaterialCatalogResponseSchema(BaseModel):
    id: int
    code: str
    name: str

    material_type: MaterialType
    unit_type: UnitType

    stock: Decimal
    minimum_stock: PositiveDecimal

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

    minimum_stock: PositiveDecimal

    components: list[CreateMaterialComponentSchema] = Field(
        default_factory=list
    )

    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=3, max_length=100),
        description: str = Form(..., max_length=255),
        company: CompanyType = Form(...),
        material_type: MaterialType = Form(...),
        unit_type: UnitType = Form(...),
        minimum_stock: PositiveDecimal = Form(...),
        components: str | None = Form(None)
    ):
        parsed_components = []

        if components:
            parsed_components = [
                CreateMaterialComponentSchema.model_validate(item)
                for item in orjson.loads(components)
            ]
        return cls(
            name=name,
            description=description,
            company=company,
            material_type=material_type,
            unit_type=unit_type,
            minimum_stock=minimum_stock,
            components=parsed_components
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

    minimum_stock: PositiveDecimal | None = None

    delete_image: bool = False

    components: list[CreateMaterialComponentSchema] | None = None

    @classmethod
    def as_form(
        cls,
        name: str | None = Form(None, min_length=3, max_length=100),
        description: str | None = Form(None, max_length=255),
        company: CompanyType | None = Form(None),
        material_type: MaterialType | None = Form(None),
        unit_type: UnitType | None = Form(None),
        minimum_stock: PositiveDecimal | None = Form(None),
        delete_image: bool = Form(False),
        components: str | None = Form(None)
    ):
        parsed_components = None

        if components is not None:
            parsed_components = [
                CreateMaterialComponentSchema.model_validate(item)
                for item in orjson.loads(components)
            ]

        return cls(
            name=name,
            description=description,
            company=company,
            material_type=material_type,
            unit_type=unit_type,
            minimum_stock=minimum_stock,
            delete_image=delete_image,
            components=parsed_components
        )