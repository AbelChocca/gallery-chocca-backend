from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict

from app.features.products.variant.variant_dto import PublishProductVariantCommand, GridProductVariantDTO, ProductVariantDTO
from app.features.products.types import BrandType, CategoryType, FitType
from app.shared.pagination.dto import PaginatedDTO, PaginationDTO

@dataclass(slots=True)
class ProductDetailDTO:
    id: int
    nombre: str
    descripcion: str

    brand: BrandType
    category: CategoryType

    fit: FitType | None
    slug: str | None

    variants: list[ProductVariantDTO] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "brand": self.brand,
            "category": self.category,
            "fit": self.fit,
            "slug": self.slug,
            "variants": [
                variant.to_dict()
                for variant in self.variants
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ProductDetailDTO":

        return cls(
            id=data["id"],
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            brand=data["brand"],
            category=data["category"],
            fit=data.get("fit"),
            slug=data.get("slug"),
            variants=[
                ProductVariantDTO.from_dict(variant)
                for variant in data["variants"]
            ],
        )

@dataclass(slots=True)
class GridProductDTO:
    id: int
    nombre: str
    category: CategoryType
    brand: BrandType
    fit: FitType
    slug: str | None

    variants: list[GridProductVariantDTO] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "category": self.category,
            "brand": self.brand,
            "fit": self.fit,
            "slug": self.slug,
            "variants": [
                variant.to_dict()
                for variant in self.variants
            ],
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            category=data["category"],
            slug=data["slug"],
            brand=data["brand"],
            fit=data["fit"],
            variants=[
                GridProductVariantDTO.from_dict(v)
                for v in data["variants"]
            ],
        )

@dataclass(slots=True)
class CatalogProductDTO(PaginatedDTO[GridProductDTO]):

    def to_dict(self) -> dict:
        return {
            "items": [
                product.to_dict()
                for product in self.items
            ],
            "total_items": self.total_items,
            "pagination": self.pagination.to_dict,
        }
    
    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "CatalogProductDTO":

        return cls(
            items=[
                GridProductDTO.from_dict(product)
                for product in data["items"]
            ],
            total_items=data["total_items"],
            pagination=PaginationDTO.from_dict(
                data["pagination"]
            )
        )

@dataclass
class UpdateProductCommand:
    id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    brand: Optional[BrandType] = None
    category: Optional[CategoryType] = None
    fit: str | None = None

    # flags
    name_changed: bool = False

    @property
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass 
class PublishProductCommand:
    nombre: str
    descripcion: str
    category: CategoryType
    brand: BrandType
    fit: str

    variants: List[PublishProductVariantCommand]

    temp_keys: List[str]
    
@dataclass
class CreateProductResponseDTO:
    id: int
    slug: str

@dataclass
class FilterProductCommand:
    name: str | None = None
    brand: BrandType | None = None
    category: CategoryType | None = None
    colors: list[str] | None = None
    sizes: List[str] | None = None
    sku: str | None = None

    @property
    def to_dict(self) -> Dict:
        return asdict(self)
    
@dataclass(slots=True)
class CountProductPerCategoryDTO:
    category: str
    total: int

@dataclass(slots=True)
class ProductsOverviewDTO:
    total: int = 0
    per_category: list[CountProductPerCategoryDTO] = field(default_factory=list)
    recent: list[dict] = field(default_factory=list)