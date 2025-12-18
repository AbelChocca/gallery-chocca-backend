from typing import Optional

from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.entities.product_variant import ProductVariant
from app.modules.product.domain.entities.variant_image import VariantImage

from app.modules.product.infra.models.product_model import (
    ProductTable,
    VariantColorTable,
    VariantImageTable
)

class ProductMapper:
    # ==========================================================
    #                 DB → ENTITY
    # ==========================================================
    @staticmethod
    def to_entity(product_db: ProductTable) -> Product:
        variants = []

        for variant in (product_db.variants or []):
            # Mapear imagenes
            images = [
                VariantImage(
                    id=img.id,
                    url=img.url,
                    cloudinary_id=img.cloudinary_id,
                    variant_id=img.variant_id
                )
                for img in (variant.imagenes or [])
            ]

            variants.append(
                ProductVariant(
                    id=variant.id,
                    product_id=variant.product_id,
                    color=variant.color,
                    tallas=variant.tallas,
                    imagenes=images
                )
            )

        return Product(
            id=product_db.id,
            nombre=product_db.nombre,
            descripcion=product_db.descripcion,
            precio=product_db.precio,
            categoria=product_db.categoria,
            modelo=product_db.modelo,
            marca=product_db.marca,
            slug=product_db.slug,
            descuento=product_db.descuento,
            promocion=product_db.promocion,
            variants=variants
        )


    @staticmethod
    def to_db_model(product: Product, existing_db: Optional[ProductTable] = None) -> ProductTable:

        # =====================================================
        #           MODO UPDATE 
        # =====================================================
        if existing_db:
            existing_db.nombre = product.nombre
            existing_db.descripcion = product.descripcion
            existing_db.precio = product.precio
            existing_db.categoria = product.categoria
            existing_db.marca = product.marca
            existing_db.modelo = product.modelo
            existing_db.slug = product.slug
            existing_db.descuento = product.descuento
            existing_db.promocion = product.promocion

            new_variants = []

            for variant in (product.variants or []):

                variant_db = VariantColorTable(
                    id=variant.id,
                    color=variant.color,
                    tallas=variant.tallas,
                    product_id=existing_db.id
                )

                variant_db.imagenes = [
                    VariantImageTable(
                        id=img.id,           # actualiza si existe
                        variant_id=variant.id,
                        url=img.url,
                        cloudinary_id=img.cloudinary_id,
                    )
                    for img in (variant.imagenes or [])
                ]

                new_variants.append(variant_db)

            existing_db.variants = new_variants
            return existing_db

        product_variants = []

        for variant in (product.variants or []):
            images_db = [
                VariantImageTable(
                    url=img.url,
                    cloudinary_id=img.cloudinary_id
                )
                for img in (variant.imagenes or [])
            ]

            variant_db = VariantColorTable(
                color=variant.color,
                tallas=variant.tallas,
                imagenes=images_db
            )

            product_variants.append(variant_db)

        return ProductTable(
            nombre=product.nombre,
            descripcion=product.descripcion,
            precio=product.precio,
            categoria=product.categoria,
            marca=product.marca,
            modelo=product.modelo,
            slug=product.slug,
            descuento=product.descuento,
            promocion=product.promocion,
            variants=product_variants
        )