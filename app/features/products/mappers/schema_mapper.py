from app.features.products.variant_size.variant_size_dto import PublishVariantSizeCommand
from app.features.inventory.dtos.inventory import CreateInventoryCommand
from app.core.constants.color_families import COLOR_FAMILY_MAP

from app.features.products.product_dto import (
    PublishProductCommand,
    PublishProductVariantCommand,
    FilterProductCommand,
)

from app.features.products.schema import (
    CreateProductSchema,
    FilterSchema,
)

class InputSchemaMapper:

    @staticmethod
    def to_publish_command(
        schema: CreateProductSchema,
    ) -> PublishProductCommand:

        product_variants = [
            PublishProductVariantCommand(
                color=variant.color,
                temp_key=variant.temp_key,
                sizes=[
                    PublishVariantSizeCommand(
                        size=size.size,
                        barcode=size.barcode,
                        inventories=[
                            CreateInventoryCommand(
                                location_id=inventory.location_id,
                                minimum_stock=inventory.minimum_stock,
                                initial_stock=inventory.initial_stock,
                            )
                            for inventory in (size.inventories or [])
                        ],
                    )
                    for size in variant.sizes
                ],
            )
            for variant in schema.variants
        ]

        return PublishProductCommand(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            brand=schema.brand,
            category=schema.category,
            base_price=schema.base_price,
            fit=schema.fit,
            variants=product_variants,
            temp_keys=schema.temp_keys,
        )
    
    @staticmethod
    def to_filter_command(schema: FilterSchema) -> FilterProductCommand:
        colors = COLOR_FAMILY_MAP.get(schema.color)
        return FilterProductCommand(
            name=schema.name,
            brand=schema.brand,
            category=schema.category,
            colors=colors,
            sizes=schema.sizes,
            sku=schema.sku
        )
