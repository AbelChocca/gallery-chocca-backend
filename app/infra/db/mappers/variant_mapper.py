from app.features.products.variant.product_variant import ProductVariant

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.products.models.model_product import VariantTable

from .variant_size_mapper import VariantSizeMapper


class VariantMapper(BaseMapper[ProductVariant, VariantTable]):

    @staticmethod
    def to_entity(model: VariantTable) -> ProductVariant:
        return ProductVariant(
            id=model.id,
            product_id=model.product_id,
            color=model.color,
            sizes=[
                VariantSizeMapper.to_entity(size)
                for size in (model.sizes or [])
            ],
        )

    @staticmethod
    def to_db_model(
        entity: ProductVariant,
        existing_model: VariantTable | None = None,
    ) -> VariantTable:

        if existing_model:

            existing_model.color = entity.color

            existing_sizes = {
                size.id: size
                for size in existing_model.sizes
                if size.id is not None
            }

            new_sizes = []

            for size_entity in entity.sizes:

                if (
                    size_entity.id is not None
                    and size_entity.id in existing_sizes
                ):

                    new_sizes.append(
                        VariantSizeMapper.to_db_model(
                            size_entity,
                            existing_sizes[size_entity.id],
                        )
                    )

                else:

                    new_sizes.append(
                        VariantSizeMapper.to_db_model(size_entity)
                    )

            existing_model.sizes = new_sizes

            return existing_model

        return VariantTable(
            color=entity.color,
            sizes=[
                VariantSizeMapper.to_db_model(size)
                for size in (entity.sizes or [])
            ],
        )