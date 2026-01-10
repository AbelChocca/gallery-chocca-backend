from app.domain.product.entities.product_variant import ProductVariant
from app.domain.product.dto.variant_dto import UpdateProductVariantDTO
from app.domain.media.entities.image import ImageEntity
from app.domain.product.exceptions.product_exception import MissingVariantsException, InvalidProductNameException, InvalidVariantImageException, CannotDeleteVariantProduct

from typing import List, Optional, Tuple, Dict, Union

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

    def add_variant(self, variant: ProductVariant) -> None:
        self.variants.append(variant)

    def update_slug(self, new_slug: str) -> None:
        self.slug = new_slug

    def get_all_variants_images_id(self) -> List[str]:
        res = []
        for variant in self.variants:
            res.extend(variant.get_all_images_public_id())
        return res
    
    def get_variants_id(self) -> List[int]:
        return [variant.id for variant in self.variants]
    
    def plan_images_and_variants_deletions(self, variants_dto: List[UpdateProductVariantDTO]) -> Tuple[List[str | None], List[int | None]]:
        res = ([], [])
        for variant in variants_dto:
            for image in variant.imagenes:
                if image.to_delete:
                    res[0].append(image.cloudinary_id)
            if variant.to_delete:
                res[1].append(variant.id)
        return res
    
    def sync_images_id(self, images: List[ImageEntity]) -> None:
        images_service_id: Dict[str, int] = {image.service_id: image.id for image in images}
        for variant in self.variants:
            variant.sync_images_id(images_service_id)
    
    def sync_variants(self, variants_dto: List[UpdateProductVariantDTO]):
        existing_variants: Dict[int, ProductVariant] = {
            variant.id: variant 
            for variant in self.variants
            if variant.id is not None
            }
        new_variants: List[ProductVariant] = []
        for variant in variants_dto:
            if variant.to_delete:
                continue

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

    def sync_images_to_variants(self, images: List[ImageEntity]) -> None:
        images_owners_id: Dict[str, ImageEntity] = {image.owner_id: image for image in images}
        for variant in self.variants:
            variant.agregar_image(images_owners_id.get(variant.id, []))

    def add_image_on_specify_variant(
            self, 
            variant_index: int,
            image_url: str,
            service_id: str
            ) -> None:
        new_image: ImageEntity = ImageEntity(
            image_url=image_url,
            owner_type="product_variant",
            service_id=service_id
        )
        self.variants[variant_index].agregar_image(new_image)

    def get_all_images_from_variants(self) -> List[ImageEntity]:
        res: List[ImageEntity] = []
        for variant in self.variants:
            res.extend(variant.get_images())
        return res

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

    def raise_invalid_variants_index(self, new_variants_index: Optional[List[int]]  = None) -> None:
        if not new_variants_index:
            return None

        for variant_idx in new_variants_index:
            if variant_idx < 0 or variant_idx >= len(self.variants):
                raise InvalidVariantImageException(f"The image with temp's variant id: {variant_idx} cannot upload cause the id didn't match the variants product length")
            
    def raise_cannot_delete_variants(self, variants_id_to_delete: List[Union[int, None]]) -> None:
       diff: int = len(self.variants) - len(variants_id_to_delete)
       if diff < 1:
           raise CannotDeleteVariantProduct(f"Product must be at least one variant, current variants count: {len(self.variants)}, variants to delete count: {len(variants_id_to_delete)}")

    def cannot_delete_image(self, images_id_to_delete: List[Union[str, None]]) -> None:
        for variant in self.variants:
            variant.raise_cannot_delete_image(images_id_to_delete)

    def get_variant_images(self, variant_id: Optional[int] = None) -> List[str]:
        if not variant_id:
            return []
        
        variant_filtered: ProductVariant = None
        for variant in self.variants:
            if variant.id == variant_id:
                variant_filtered = variant
                break
        if not variant_filtered:
            return None
        
        return variant_filtered.get_all_images_public_id()

    @staticmethod
    def get_filter_key(
            category: Optional[str] = None,
            brand: Optional[str] = None,
            model: Optional[str] = None,
            id: Optional[int] = None,
            promotion: Optional[bool] = None,
            color: Optional[str] = None,
            name: Optional[str] = None
    ) -> str:
        key: str = "products"

        if name:
            key += f"/related:{name}"
        if brand:
            key += f"/brand:{brand}"
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
