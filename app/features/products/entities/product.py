from app.features.products.entities.product_variant import ProductVariant
from app.features.products.dto.product_dto import CategoryType, BrandType
from app.features.products.dto.variant_dto import UpdateProductVariantCommand, PublishProductVariantCommand
from app.features.media.entities.image import ImageEntity

from typing import List, Dict, Any
from decimal import Decimal
from app.core.exceptions import ValidationError

class Product:
    _UPDATABLE_FIELDS = {"nombre", "descripcion", "category", "fit", "brand"}

    def __init__(
            self,
            nombre: str,
            descripcion: str,
            category: CategoryType,
            slug: str,
            variants: List[ProductVariant],
            base_price: Decimal,
            is_active: bool,
            brand: BrandType,
            fit: str | None = None,
            id: int | None = None,
    ):        
        # validation
        for v in [nombre, brand, category]:
            self._not_number(v)    

        for v in [nombre, descripcion]:
            v = self._not_empty(v)

        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.category = category
        self._base_price = base_price
        self.brand = brand
        self.is_active = is_active
        self._variants = variants
        self.fit = fit
        self._slug = slug

    @property
    def base_price(self) -> Decimal:
        return self._base_price
    
    @base_price.setter
    def price(self, new_price: Decimal) -> None:
        self._base_price = new_price

    @property
    def variants(self) -> List[ProductVariant]:
        return self._variants
    
    @variants.setter
    def variants(self, new_variants: List[ProductVariant]) -> None:
        self._variants = new_variants

    @property
    def slug(self) -> str:
        return self._slug

    @slug.setter
    def slug(self, new_slug: str) -> None:
        if not isinstance(new_slug, str):
            raise ValidationError(
                "'new_slug' must be a string",
                {
                    "entity": "Product",
                    "event": "slug.setter",
                    "new_slug_type": type(new_slug).__name__
                }
                )
        self._slug = new_slug

    @property
    def all_image_public_ids(self) -> List[str]:
        return [
            public_id
            for variant in self.variants
            for public_id in variant.all_images_public_ids
        ]

    @property
    def variant_ids(self) -> List[int]:
        return [variant.id for variant in self.variants if variant.id]
    
    @property
    def has_new_images(self) -> bool:
        for variant in self.variants:
            if any(
                image.owner_id is None
                or image.id is None
                for image in variant.imagenes
            ):
                return True
        return False
    
    @property
    def has_variants(self) -> bool:
        return len(self.variants) > 0
    
    @property
    def all_variant_images(self) -> List[ImageEntity]:
        return [
            image 
            for variant in self.variants
            for image in variant.imagenes
        ]
    
    @property
    def images_without_id(self) -> List[ImageEntity]:
        return [
            image
            for variant in self.variants
            for image in variant.images_without_id
        ]
    
    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "category": self.category,
            "slug": self.slug,
            "brand": self.brand,
            "fit": self.fit,
            "variants": [
                variant.to_dict
                for variant in self.variants
            ]
        }
    
    @property
    def to_inventory_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "category": self.category,
            "brand": self.brand,
            "fit": self.fit,
            "variants": [
                variant.to_inventory_dict
                for variant in self.variants
            ]
        }
    
    def get_variant_images(self, variant_id: int) -> List[str]:
        if not variant_id:
            return []
        if variant_id <= 0:
            raise ValidationError(
                "'variant_id' must be greater than 0",
                {
                    "entity": "Product",
                    "event": "get_variant_images",
                    "variant_id": variant_id
                }
            )
        
        variant_filtered: ProductVariant = None
        for variant in self.variants:
            if variant.id == variant_id:
                variant_filtered = variant
                break
        if not variant_filtered:
            return []
        
        return variant_filtered.all_images_public_ids
    
    def sync_existing_variants(self, variants_dto: List[UpdateProductVariantCommand]):
        existing_variants: Dict[int, ProductVariant] = {
            variant.id: variant 
            for variant in self.variants
            if variant.id is not None
            }
        new_variants = []
        for variant in variants_dto:
            if variant.to_delete:
                continue

            if variant.id is not None and variant.id in existing_variants:
                prev_variant = existing_variants[variant.id]
                prev_variant.update_variant(
                    color=variant.color,
                    sizes=variant.sizes
                )
                new_variants.append(prev_variant)
        self.variants = new_variants

    def add_variant(
            self,
            *,
            variant_command: PublishProductVariantCommand,
            images: List[ImageEntity] | None = None,
    ) -> None:
        variant = ProductVariant(
                color=variant_command.color,
                product_id=self.id or None
            )
        for size in variant_command.sizes:
            variant.add_new_size(
                size=size,
                product_name=self.nombre,
                variant_color=variant_command.color,
                initial_stock=size.initial_stock
            )
        variant.imagenes = images or []
        self.variants.append(variant)

    def sync_images_to_variants(
            self, 
            images_by_owner_id: Dict[int, List[ImageEntity]]
        ) -> None:
        for variant in self.variants:
            variant.imagenes = images_by_owner_id.get(variant.id, [])

    def update_product(self, new_product_obj: Dict[str, Any]) -> None:
        if not isinstance(new_product_obj, dict):
            raise ValidationError(
                "'new_product_obj' must be a dict",
                {
                    "entity": "Product",
                    "event": "add_image_on_existing_variant",
                    "invalid_prop_type": type(new_product_obj).__name__
                }
            )
        if not new_product_obj:
            return None

        for key, value in new_product_obj.items():
            if key == "variants":
                continue

            if key not in self._UPDATABLE_FIELDS:
                continue

            if value is None:
                continue

            setattr(self, key, value)

    def _not_number(self, v: str) -> None:
        if any(c.isdigit() for c in v):
            raise ValidationError(
                "Value can't have any digit",
                {
                    "event": '_not_number/validator',
                    "module": "product"
                }
            )
        
    def _not_empty(self, v: str | None) -> str:
        if v is None: 
            return None
        
        if not v.strip():
            raise ValidationError(
                "Value cannot be empty",
                {
                    "event": '_not_empty/validator',
                    "module": "product"
                }
            )
    
        return v.strip()
                
    def __str__(self):
        res = "=== PRODUCT ===\n"
        res += (
            f"Name: {self.nombre}\n"
            f"Description: {self.descripcion[:55]}\n"
            f"Category: {self.category}\n"
            f"Brand: {self.brand}\n"
            f"Fit: {self.fit}\n"
        )
        if self.has_variants:
            res += "\t=== Variants ===\n"
            for variant in self.variants:
                res += str(variant)

        return res