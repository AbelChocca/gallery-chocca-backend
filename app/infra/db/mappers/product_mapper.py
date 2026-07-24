from app.features.products.product import Product

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.products.models.model_product import ProductTable

from .variant_mapper import VariantMapper


class ProductMapper(BaseMapper[Product, ProductTable]):

    @staticmethod
    def to_entity(model: ProductTable) -> Product:

        return Product(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            category=model.category,
            fit=model.fit,
            base_price=model.base_price,
            is_active=model.is_active,
            brand=model.brand,
            slug=model.slug,
            variants=[
                VariantMapper.to_entity(v)
                for v in (model.variants or [])
            ],
        )

    @staticmethod
    def to_db_model(
        entity: Product,
        existing_model: ProductTable | None = None,
    ) -> ProductTable:

        if existing_model:

            existing_model.nombre = entity.nombre
            existing_model.descripcion = entity.descripcion
            existing_model.category = entity.category
            existing_model.brand = entity.brand
            existing_model.fit = entity.fit
            existing_model.slug = entity.slug
            existing_model.is_active = entity.is_active
            existing_model.base_price = entity.base_price

            existing_variants = {
                variant.id: variant
                for variant in existing_model.variants
                if variant.id is not None
            }

            new_variants = []

            for variant_entity in entity.variants:

                if (
                    variant_entity.id is not None
                    and variant_entity.id in existing_variants
                ):

                    new_variants.append(
                        VariantMapper.to_db_model(
                            variant_entity,
                            existing_variants[variant_entity.id],
                        )
                    )

                else:

                    new_variants.append(
                        VariantMapper.to_db_model(variant_entity)
                    )

            existing_model.variants = new_variants

            return existing_model

        return ProductTable(
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            category=entity.category,
            brand=entity.brand,
            base_price=entity.base_price,
            is_active=entity.is_active,
            fit=entity.fit,
            slug=entity.slug,
            variants=[
                VariantMapper.to_db_model(v)
                for v in (entity.variants or [])
            ],
        )