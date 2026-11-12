from dataclasses import dataclass, asdict, field
from typing import List, Dict
from decimal import Decimal

from app.features.products.variant.variant_dto import PublishProductVariantCommand, GridProductVariantDTO, ProductVariantDTO
from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO, PromotionApplicationScope
from app.features.products.types import BrandType, CategoryType, FitType
from app.shared.pagination.dto import PaginatedDTO, PaginationDTO

@dataclass(slots=True)
class ProductDetailDTO:
    id: int
    nombre: str
    descripcion: str

    brand: BrandType
    category: CategoryType

    base_price: Decimal

    fit: FitType | None
    slug: str | None

    variants: list[ProductVariantDTO] = field(default_factory=list)

    discount_price: Decimal | None = None
    final_price: Decimal | None = None

    applied_promotions: list[AppliedPromotionDTO] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "brand": self.brand,
            "category": self.category,
            "base_price": str(self.base_price),
            "fit": self.fit,
            "slug": self.slug,
            "variants": [
                variant.to_dict()
                for variant in self.variants
            ],
            "discount_price": (
                str(self.discount_price)
                if self.discount_price is not None
                else None
            ),
            "final_price": (
                str(self.final_price)
                if self.final_price is not None
                else None
            ),
            "applied_promotions": [
                {
                    "promotion_id": promo.promotion_id,
                    "name": promo.name,
                    "discount_amount": str(promo.discount_amount),
                    "application_scope": (
                        promo.application_scope.value
                        if promo.application_scope is not None
                        else None
                    ),
                    "coupon_code": promo.coupon_code,
                }
                for promo in self.applied_promotions
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
            base_price=Decimal(data["base_price"]),
            brand=BrandType(data["brand"]),
            category=CategoryType(data["category"]),
            fit=(
                FitType(data["fit"])
                if data.get("fit") is not None
                else None
            ),
            slug=data.get("slug"),
            variants=[
                ProductVariantDTO.from_dict(variant)
                for variant in data["variants"]
            ],
            discount_price=(
                Decimal(data["discount_price"])
                if data.get("discount_price") is not None
                else None
            ),
            final_price=(
                Decimal(data["final_price"])
                if data.get("final_price") is not None
                else None
            ),
            applied_promotions=[
                AppliedPromotionDTO(
                    promotion_id=promo["promotion_id"],
                    name=promo["name"],
                    discount_amount=Decimal(
                        promo["discount_amount"]
                    ),
                    application_scope=(
                        PromotionApplicationScope(
                            promo["application_scope"]
                        )
                        if promo.get("application_scope") is not None
                        else None
                    ),
                    coupon_code=promo.get("coupon_code"),
                )
                for promo in data.get("applied_promotions", [])
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
class PublishProductCommand:
    nombre: str
    descripcion: str
    category: CategoryType
    base_price: Decimal
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