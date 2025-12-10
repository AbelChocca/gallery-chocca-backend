from app.modules.product.domain.entities.variant_color import VariantColor
from app.modules.product.domain.entities.variant_image import VariantImage
from app.shared.exceptions.domain.product_exception import MissingVariantsException, InvalidProductNameException, InvalidDiscountPercentException
from app.shared.dto.product_dto import UpdateProductDTO
from app.shared.dto.color_variant_dto import UpdateProductColorVariantDTO

from typing import List, Optional
from slugify import slugify
from dataclasses import asdict

class Product:
    def __init__(
            self,
            nombre: str,
            descripcion: str,
            precio: float,
            categoria: str,
            variants: List[VariantColor],
            modelo: Optional[str] = None,
            slug: Optional[str] = None,
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
        self.slug = slugify(nombre)

    def apply_discount(self, discount_percent: float):
        if discount_percent < 0 or discount_percent > 100:
            raise InvalidDiscountPercentException()
        self.descuento = (self.precio * discount_percent) / 100

    def set_promotion(self, toggle: bool):
        self.promocion = toggle

    def _update_variants(self, variants: List[UpdateProductColorVariantDTO]) -> None:
        existing_variants = {variant.id: variant for variant in self.variants}

        for variant in variants:
            if variant.id in existing_variants:
                existing_var = existing_variants[variant.id]
                existing_var.update_variant(variant)
            else:
                imagenes = [
                    VariantImage(
                        url=image.url,
                        cloudinary_id=image.cloudinary_id
                    )
                    for image in variant.imagenes
                ]
                self.variants.append(
                    VariantColor(
                        color=variant.color,
                        tallas=variant.tallas,
                        imagenes=imagenes
                    )
                )
    def update_product(self, new_product: UpdateProductDTO):
        self._update_variants(new_product.variants)

        update = {k:v for k, v in asdict(new_product).items() if v is not None and k != "variants"}
        for k, v in update.items():
            setattr(self, k, v)
            

    @staticmethod
    def _verify_created_product(
        nombre: str,
        variants: List['VariantColor']
    ) -> None:
        if len(nombre) < 6:
            raise InvalidProductNameException()
        if not variants:
            raise MissingVariantsException()
