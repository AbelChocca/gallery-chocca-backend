from dataclasses import dataclass, asdict
from typing import List, Optional, Dict

from app.features.products.dto.variant_dto import UpdateProductVariantCommand, PublishProductVariantCommand
from app.features.products.types import BrandType, CategoryType

@dataclass
class UpdateProductCommand:
    variants: List[UpdateProductVariantCommand]

    id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[BrandType] = None
    categoria: Optional[CategoryType] = None
    model_family: Optional[str] = None
    fit: str | None = None
    temp_keys: List[str] | None = None

    # flags
    name_changed: bool = False

    @property
    def to_dict(self) -> dict:
        return asdict(self)
    
    @property
    def has_all_variants_deleted(self) -> bool:
        return all(
            v.to_delete
            for v in self.variants
        )
    
    @property
    def has_new_images(self) -> bool:
        return bool(self.temp_keys)
    
    @property
    def new_images_per_variant(self) -> dict[str, int]:
        images_count_per_temp_key = {variant.temp_key: 0 for variant in self.variants}
        for t_key in (self.temp_keys or []):
            images_count_per_temp_key[t_key] += 1
        return images_count_per_temp_key
    
    @property
    def new_variants(self) -> list:
        return [
            variant
            for variant in self.variants
            if variant.temp_key.startswith('temp')
        ]
    
    @property
    def existing_variants_count(self) -> int:
        return sum(
            1
            for v in self.variants
            if v.id is not None
        )
    
    @property
    def variants_to_delete_count(self) -> int:
        return sum(
            1
            for v in self.variants
            if v.id is not None and v.to_delete
        )
    
    @property
    def new_variants_count(self) -> int:
        return sum(
            1
            for v in self.variants
            if v.id is None
        )

@dataclass 
class PublishProductCommand:
    nombre: str
    descripcion: str
    categoria: CategoryType
    marca: BrandType
    model_family: str
    fit: str

    variants: List[PublishProductVariantCommand]

    temp_keys: List[str]
    
@dataclass
class CreateProductResponse:
    id: int
    slug: str

@dataclass
class FilterProductCommand:
    name: str | None = None
    marca: BrandType | None = None
    categoria: CategoryType | None = None
    model_family: str | None = None
    colors: list[str] | None = None
    sizes: List[str] | None = None
    sku: str | None = None

    @property
    def to_dict(self) -> Dict:
        return asdict(self)