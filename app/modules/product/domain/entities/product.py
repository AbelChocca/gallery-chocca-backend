from app.modules.product.domain.entities.product_variant import ProductVariant
from app.modules.product.domain.dto.variant_dto import UpdateProductVariantDTO
from app.modules.product.domain.exceptions.product_exception import MissingVariantsException, InvalidProductNameException, InvalidDiscountPercentException, InvalidVariantImageException

from typing import List, Optional, Tuple, Dict

class Product:
    def __init__(
            self,
            nombre: str,
            descripcion: str,
            precio: float,
            categoria: str,
            slug: str,
            variants: List[ProductVariant],
            modelo: Optional[str] = None,
            id: Optional[int] = None,
            descuento: Optional[float] = 0.0,
            marca: Optional[str] = None,
            promocion: bool = False
    ):
        self._verify_created_product(
            nombre=nombre,
            variants=variants
        )

        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.marca = marca
        self.descuento = descuento
        self.promocion = promocion
        self.variants = variants
        self.modelo = modelo
        self.slug = slug

    def apply_discount(self, discount_percent: float):
        if discount_percent < 0 or discount_percent > 100:
            raise InvalidDiscountPercentException()
        self.descuento = (self.precio * discount_percent) / 100

    def set_promotion(self, toggle: bool):
        self.promocion = toggle

    def add_variant(self, variant: ProductVariant) -> None:
        self.variants.append(variant)

    def update_slug(self, new_slug: str) -> None:
        self.slug = new_slug

    def get_all_variants_images_id(self) -> List[str]:
        res = []
        for variant in self.variants:
            res.extend(variant.get_all_images_id())
        return res
    
    def plan_images_and_variants_deletions(self, variants_dto: List[UpdateProductVariantDTO]) -> Tuple[List[str | None], List[int | None]]:
        res = ([], [])
        for variant in variants_dto:
            for image in variant.imagenes:
                if image.to_delete:
                    res[0].append(image.cloudinary_id)
            if variant.to_delete:
                res[1].append(variant.id)
        return res
    
    def sync_variants(self, variants_dto: List[UpdateProductVariantDTO]):
        existing_variants: Dict[int, ProductVariant] = {
            variant.id: variant 
            for variant in self.variants
            if variant.id is not None
            }
        new_variants: List[ProductVariant] = []
        for variant in variants_dto:
            if variant.id not in existing_variants:
                new_variants.append(
                    ProductVariant(
                        color=variant.color,
                        tallas=variant.tallas
                    )
                )
            else:
                prev_variant = existing_variants[variant.id]
                prev_variant.update_variant(
                    color=variant.color,
                    tallas=variant.tallas
                )
                new_variants.append(prev_variant)
        self.variants = new_variants

    def add_image_on_specify_variant(
            self, 
            variant_index: int,
            url: str,
            public_id: str
            ) -> None:
        self.variants[variant_index].agregar_image(
            image_url=url,
            public_id=public_id
        )
    def update_product(
            self,
            nombre: Optional[str] = None,
            descripcion: Optional[str] = None,
            precio: Optional[float] = None,
            categoria: Optional[str] = None,
            modelo: Optional[str] = None,
            descuento: Optional[float] = None,
            marca: Optional[str] = None,
            promocion: Optional[bool] = None
            ) -> None:
        self.nombre = nombre if nombre is not None else self.nombre
        self.descripcion = descripcion if descripcion is not None else self.descripcion
        self.precio = precio if precio is not None else self.precio
        self.categoria = categoria if categoria is not None else self.categoria
        self.modelo = modelo if modelo is not None else self.modelo
        self.descuento = descuento if descuento is not None else self.descuento
        self.marca = marca if marca is not None else self.marca
        self.promocion = promocion if promocion is not None else self.promocion

    def raise_invalid_variants_index(self, new_variants_index: List[int]) -> None:
        for variant_idx in new_variants_index:
            if variant_idx < 0 or variant_idx >= len(self.variants):
                raise InvalidVariantImageException(f"The image with temp's variant id: {variant_idx} cannot upload cause the id didn't match the variants product length")

    @staticmethod
    def get_filter_key(
            category: Optional[str] = None,
            model: Optional[str] = None,
            id: Optional[int] = None,
            promotion: Optional[bool] = None,
            color: Optional[str] = None,
            name: Optional[str] = None
    ) -> str:
        key: str = "products"

        if name:
            key += f"/related:{name}"
        if category:
            key += f"/category:{category}"
        if model:
            key += f"/model:{model}"
        if id:
            key += f"/{id}"
        if promotion:
            key += f"/promotion:true" if promotion is True else f":promotion:false"
        if color:
            key += f"/color:{color}"
        return key

    @staticmethod
    def _verify_created_product(
        nombre: str,
        variants: List['ProductVariant']
    ) -> None:
        if len(nombre) < 6:
            raise InvalidProductNameException()
        if not variants:
            raise MissingVariantsException()
        
    def debug_snapshot(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "slug": self.slug,
            "variants": [
                {
                    "id": variant.id,
                    "color": variant.color,
                    "imagenes": len(variant.imagenes)
                }
                for variant in self.variants
            ]
        }
