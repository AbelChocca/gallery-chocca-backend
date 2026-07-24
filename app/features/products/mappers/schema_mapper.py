from app.features.products.variant_size.variant_size_dto import PublishVariantSizeCommand
from app.features.inventory.dtos.inventory import CreateInventoryCommand
from app.core.constants.color_families import COLOR_FAMILY_MAP

from app.features.products.schema import (
    ProductRead,
    GridProductRead,
    GetGridProductsResponse,
)
from app.features.products.product_dto import (
    CatalogProductDTO,
    GridProductDTO,
    ProductDetailDTO,
    PublishProductCommand,
    PublishProductVariantCommand,
    FilterProductCommand,
    UpdateProductCommand
)

from app.features.products.schema import (
    ProductRead,
    GridProductRead,
    GetGridProductsResponse,
    CreateProductSchema,
    FilterSchema,
    UpdateProductSchema
)


class OutputSchemaMapper:

    @staticmethod
    def to_product_read(dto: ProductDetailDTO) -> ProductRead:
        return ProductRead.model_validate(dto)

    @staticmethod
    def to_grid_product_read(dto: GridProductDTO) -> GridProductRead:
        return GridProductRead.model_validate(dto)

    @staticmethod
    def to_grid_products_response(
        dto: CatalogProductDTO,
    ) -> GetGridProductsResponse:

        return GetGridProductsResponse(
            products=[
                OutputSchemaMapper.to_grid_product_read(product)
                for product in dto.items
            ],
            total_items=dto.total_items,
            pagination=dto.pagination,
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
            fit=schema.fit,
            variants=product_variants,
            temp_keys=schema.temp_keys,
        )
    
    @staticmethod
    def to_update_command(schema: UpdateProductSchema) -> UpdateProductCommand:

        return UpdateProductCommand(
            id=schema.id,
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            brand=schema.brand,
            category=schema.category,
            fit=schema.fit,
            name_changed=schema.name_changed,
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
