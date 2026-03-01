from app.domain.product.entities.product import Product
from app.domain.product.entities.product_variant import ProductVariant
from app.domain.product.entities.variant_size import VariantSize

from app.infra.db.mappers.base_mapper import BaseMapper

from app.infra.db.models.model_product import (
    ProductTable,
    VariantTable,
    VariantSizeTable
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
                    sizes=[
                        VariantSize(
                            size=variant_size.size,
                            id=variant_size.id,
                            variant_id=variant_size.variant_id
                        )
                        for variant_size in (variant.sizes or [])
                    ]
                )
            )

        return Product(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            categoria=model.categoria,
            model_family=model.model_family,
            fit=model.fit,
            marca=model.marca,
            slug=model.slug,
            variants=variants
        )


    @staticmethod
    def to_db_model(entity: Product, existing_model: ProductTable | None = None) -> ProductTable:

        # =====================================================
        #           MODO UPDATE 
        # =====================================================
        if existing_model:
            existing_model.nombre = entity.nombre
            existing_model.descripcion = entity.descripcion
            existing_model.categoria = entity.categoria
            existing_model.marca = entity.marca
            existing_model.model_family = entity.model_family
            existing_model.fit = entity.fit
            existing_model.slug = entity.slug

            new_variants = []

            for variant in (entity.variants or []):

                variant_db = VariantTable(
                    id=variant.id,
                    color=variant.color,
                    sizes=[
                        VariantSizeTable(
                            id=variant_size.id,
                            variant_id=variant_size.variant_id,
                            size=variant_size.size
                        )
                        for variant_size in (variant.sizes or [])
                    ],
                    product_id=existing_model.id
                )

                new_variants.append(variant_db)

            existing_model.variants = new_variants
            return existing_model

        product_variants = []

        for variant in (entity.variants or []):

            variant_db = VariantTable(
                color=variant.color,
                sizes=[
                    VariantSizeTable(
                        size=variant_size.size
                    )
                    for variant_size in (variant.sizes or [])
                ]
            )

            product_variants.append(variant_db)

        return ProductTable(
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            categoria=entity.categoria,
            marca=entity.marca,
            model_family=entity.model_family,
            fit=entity.fit,
            slug=entity.slug,
            variants=product_variants
        )