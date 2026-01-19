from typing import Optional

from app.domain.product.entities.product import Product
from app.domain.product.entities.product_variant import ProductVariant

from app.infra.db.mappers.base_mapper import BaseMapper

from app.infra.db.models.model_product import (
    ProductTable,
    VariantColorTable,
)

class ProductMapper(BaseMapper[Product, ProductTable]):
    # ==========================================================
    #                 DB → ENTITY
    # ==========================================================
    @staticmethod
    def to_entity(model: ProductTable) -> Product:
        variants = []

        for variant in (model.variants or []):

            variants.append(
                ProductVariant(
                    id=variant.id,
                    product_id=variant.product_id,
                    color=variant.color,
                    tallas=variant.tallas
                )
            )

        return Product(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            precio=model.precio,
            categoria=model.categoria,
            modelo=model.modelo,
            marca=model.marca,
            slug=model.slug,
            descuento=model.descuento,
            promocion=model.promocion,
            variants=variants
        )


    @staticmethod
    def to_db_model(entity: Product, existing_model: Optional[ProductTable] = None) -> ProductTable:

        # =====================================================
        #           MODO UPDATE 
        # =====================================================
        if existing_model:
            existing_model.nombre = entity.nombre
            existing_model.descripcion = entity.descripcion
            existing_model.precio = entity.precio
            existing_model.categoria = entity.categoria
            existing_model.marca = entity.marca
            existing_model.modelo = entity.modelo
            existing_model.slug = entity.slug
            existing_model.descuento = entity.descuento
            existing_model.promocion = entity.promocion

            new_variants = []

            for variant in (entity.variants or []):

                variant_db = VariantColorTable(
                    id=variant.id,
                    color=variant.color,
                    tallas=variant.tallas,
                    product_id=existing_model.id
                )

                new_variants.append(variant_db)

            existing_model.variants = new_variants
            return existing_model

        product_variants = []

        for variant in (entity.variants or []):

            variant_db = VariantColorTable(
                color=variant.color,
                tallas=variant.tallas
            )

            product_variants.append(variant_db)

        return ProductTable(
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            precio=entity.precio,
            categoria=entity.categoria,
            marca=entity.marca,
            modelo=entity.modelo,
            slug=entity.slug,
            descuento=entity.descuento,
            promocion=entity.promocion,
            variants=product_variants
        )