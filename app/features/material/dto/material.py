from dataclasses import dataclass, field
from app.features.material.entities.material import Material
from app.features.media.entities.image import ImageEntity
from app.shared.pagination.dto import PaginatedDTO, PaginationDTO
from app.features.media.dto import ReadMediaImageDTO
from datetime import datetime
from decimal import Decimal

from app.features.material.dto.material_component import MaterialComponentDTO, CreateMaterialComponentDTO
from app.features.inventory.dtos.inventory import CreateInventoryCommand

from app.features.material.types import (
    MaterialType,
    UnitType
)
from app.shared.types import CompanyType
from app.features.inventory.types.inventory import AvailabilityStatus

@dataclass(slots=True)
class MaterialResponseDTO:
    id: int
    code: str
    name: str

    company: CompanyType
    material_type: MaterialType
    unit_type: UnitType

    stock: Decimal
    minimum_stock: Decimal

    is_active: bool

    availability_status: AvailabilityStatus

    created_at: datetime
    updated_at: datetime

    image: ReadMediaImageDTO | None = None
    description: str | None = None

    components: list[MaterialComponentDTO] | None = None

    @classmethod
    def from_entities(
        cls,
        material: Material,
        image: ImageEntity | None = None
    ) -> "MaterialResponseDTO":
        return cls(
            id=material.id,
            code=material.code,
            name=material.name,
            description=material.description,
            company=material.company,
            material_type=material.material_type,
            unit_type=material.unit_type,
            stock=material.stock,
            minimum_stock=material.minimum_stock,
            is_active=material.is_active,
            availability_status=material.availability_status,
            image=(
                ReadMediaImageDTO.from_entity(image)
                if image
                else None
            ),
            created_at=material.created_at,
            updated_at=material.updated_at,
            components=[
                MaterialComponentDTO.from_entity(component)
                for component in material.components
            ]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "company": self.company.value,
            "material_type": self.material_type.value,
            "unit_type": self.unit_type.value,
            "stock": str(self.stock),
            "minimum_stock": str(self.minimum_stock),
            "is_active": self.is_active,
            "availability_status": self.availability_status.value,
            "image": (
                self.image.to_dict()
                if self.image
                else None
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "components": [
                component.to_dict()
                for component in self.components
            ]
            if self.components
            else [],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MaterialResponseDTO":
        return cls(
            id=data["id"],
            code=data["code"],
            name=data["name"],
            description=data.get("description"),
            company=CompanyType(data["company"]),
            material_type=MaterialType(data["material_type"]),
            unit_type=UnitType(data["unit_type"]),
            stock=Decimal(data["stock"]),
            minimum_stock=Decimal(data["minimum_stock"]),
            is_active=data["is_active"],
            availability_status=AvailabilityStatus(
                data["availability_status"]
            ),
            image=(
                ReadMediaImageDTO.from_dict(data["image"])
                if data.get("image")
                else None
            ),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            components=[
                MaterialComponentDTO.from_dict(component)
                for component in data.get("components", [])
            ],
        )

@dataclass(slots=True)
class MaterialCatalogDTO:
    id: int
    code: str
    name: str
    material_type: str
    stock: Decimal
    minimum_stock: Decimal
    unit_type: str
    availability_status: AvailabilityStatus

    is_active: bool
    image: ReadMediaImageDTO | None = None

    @classmethod
    def from_entities(
        cls,
        material: Material,
        image: ImageEntity | None = None
    ) -> "MaterialCatalogDTO":

        return cls(
            id=material.id,
            code=material.code,
            name=material.name,
            material_type=material.material_type.value,
            unit_type=material.unit_type.value,
            stock=material.stock,
            minimum_stock=material.minimum_stock,
            availability_status=material.availability_status,
            is_active=material.is_active,
            image=(
                ReadMediaImageDTO.from_entity(image)
                if image
                else None
            )
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "material_type": self.material_type,
            "stock": str(self.stock),
            "minimum_stock": str(self.minimum_stock),
            "unit_type": self.unit_type,
            "availability_status": self.availability_status.value,
            "is_active": self.is_active,
            "image": (
                self.image.to_dict()
                if self.image
                else None
            )
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MaterialCatalogDTO":
        return cls(
            id=data["id"],
            code=data["code"],
            name=data["name"],
            material_type=data["material_type"],
            stock=Decimal(data["stock"]),
            minimum_stock=Decimal(data["minimum_stock"]),
            availability_status=AvailabilityStatus(
                data["availability_status"]
            ),
            unit_type=data["unit_type"],
            is_active=data["is_active"],
            image=(
                ReadMediaImageDTO.from_dict(data["image"])
                if data["image"]
                else None
            )
        )
    
class MaterialCatalogPaginatedDTO(
    PaginatedDTO[MaterialCatalogDTO]
):
    def to_dict(self) -> dict:
        return {
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "total_items": self.total_items,
            "pagination": {
                "current_page": self.pagination.current_page,
                "total_pages": self.pagination.total_pages,
            }
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ) -> "MaterialCatalogPaginatedDTO":
        return cls(
            items=[
                MaterialCatalogDTO.from_dict(item)
                for item in data["items"]
            ],
            total_items=data["total_items"],
            pagination=PaginationDTO(
                current_page=data["pagination"]["current_page"],
                total_pages=data["pagination"]["total_pages"],
            )
        )

class MaterialPaginatedDTO(
    PaginatedDTO[Material]
):
    pass

@dataclass(slots=True)
class UpdateMaterialDTO:
    name: str | None = None
    description: str | None = None
    company: CompanyType | None = None
    material_type: MaterialType | None = None
    unit_type: UnitType | None = None
    delete_image: bool = False
    components: list[CreateMaterialComponentDTO] | None = None

@dataclass(slots=True)
class CreateMaterialDTO:
    name: str
    description: str | None
    company: CompanyType
    material_type: MaterialType
    unit_type: UnitType
    components: list[CreateMaterialComponentDTO] = field(
    default_factory=list
)

    inventories: list[CreateInventoryCommand] = field(
        default_factory=list
    )

@dataclass(slots=True)
class MaterialFilters:
    search: str | None = None

    company: CompanyType | None = None

    material_type: MaterialType | None = None

    is_active: bool | None = None

    @property
    def to_dict(self) -> dict:
        return {
            "search": self.search,
            "company": self.company,
            "material_type": self.material_type,
            "is_active": self.is_active,
        }