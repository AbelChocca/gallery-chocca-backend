from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict
from decimal import Decimal

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

    original_price: Decimal = Decimal("0")
    final_price: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")

    variants: list[GridProductVariantDTO] = field(
        default_factory=list
    )

    @property
    def has_discount(self) -> bool:
        return self.discount_amount > 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "category": self.category.value,
            "brand": self.brand.value,
            "fit": self.fit.value,
            "slug": self.slug,
            "original_price": str(
                self.original_price
            ),
            "final_price": str(
                self.final_price
            ),
            "discount_amount": str(
                self.discount_amount
            ),
            "has_discount": self.has_discount,
            "variants": [
                variant.to_dict()
                for variant in self.variants
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "GridProductDTO":
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            category=CategoryType(
                data["category"]
            ),
            brand=BrandType(
                data["brand"]
            ),
            fit=FitType(
                data["fit"]
            ),
            slug=data["slug"],
            original_price=Decimal(
                data["original_price"]
            ),
            final_price=Decimal(
                data["final_price"]
            ),
            discount_amount=Decimal(
                data["discount_amount"]
            ),
            variants=[
                GridProductVariantDTO.from_dict(
                    variant
                )
                for variant in data["variants"]
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

@dataclass(frozen=True, slots=True)
class ProductSearchOptionDTO:
    id: int
    name: str
    description: str
    brand: BrandType
    category: CategoryType
    base_price: Decimal