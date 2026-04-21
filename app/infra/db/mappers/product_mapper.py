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
                            variant_id=variant_size.variant_id,
                            stock=variant_size.stock,
                            sku=variant_size.sku
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
            existing_variants_map = {
                v.id: v for v in existing_model.variants if v.id is not None
            }

            for variant in (entity.variants or []):
                if variant.id is not None and variant.id in existing_variants_map:
                    variant_db = existing_variants_map[variant.id]

                    variant_db.color = variant.color

                    existing_sizes_map = {s.id: s for s in variant_db.sizes}
                    new_sizes = []

                    for size_entity in variant.sizes:
                        if size_entity.id in existing_sizes_map:
                            new_sizes.append(existing_sizes_map[size_entity.id])
                        else:
                            new_sizes.append(
                                VariantSizeTable(
                                    size=size_entity.size,
                                    stock=size_entity.stock,
                                    sku=size_entity.sku
                                )
                            )
                    variant_db.sizes = new_sizes
                    
                    new_variants.append(variant_db)
                else:
                    variant_db = VariantTable(
                        color=variant.color,
                        sizes=[
                            VariantSizeTable(
                                size=variant_size.size,
                                stock=variant_size.stock,
                                sku=variant_size.sku
                            )
                            for variant_size in (variant.sizes or [])
                        ],
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