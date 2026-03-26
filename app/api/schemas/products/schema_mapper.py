from app.api.schemas.products.schema import CreateProductSchema, FilterSchema, UpdateProductSchema
from app.domain.product.dto.product_dto import PublishProductCommand, PublishProductVariantCommand, UpdateProductCommand, UpdateProductVariantCommand, FilterProductCommand
from app.domain.product.dto.variant_size_dto import UpdateVariantSizeCommand, PublishVariantSizeCommand
from app.domain.media.media_dto import UpdateImageCommand
from app.core.constants.color_families import COLOR_FAMILY_MAP

class InputSchemaMapper:
    @staticmethod
    def to_publish_command(schema: CreateProductSchema) -> PublishProductCommand:
        product_variants = [
            PublishProductVariantCommand(
                color=v.color,
                sizes=[
                    PublishVariantSizeCommand(
                        size=variant_size.size
                    )
                    for variant_size in v.sizes
                ],
                temp_key=v.temp_key
            )
            for v in schema.variants
        ]

        return PublishProductCommand(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            marca=schema.marca,
            categoria=schema.categoria,
            model_family=schema.model_family,
            fit=schema.fit,
            variants=product_variants,
            temp_keys=schema.temp_keys
            
        )
    @staticmethod
    def to_update_command(schema: UpdateProductSchema) -> UpdateProductCommand:
        product_variants = None

        if schema.variants:
            product_variants = [
                UpdateProductVariantCommand(
                    id=v.id,
                    product_id=v.product_id,
                    color=v.color,
                    sizes=(
                        [
                            UpdateVariantSizeCommand(
                                size=variant_size.size,
                                id=variant_size.id,
                                variant_id=variant_size.variant_id,
                                to_delete=variant_size.to_delete
                            )
                            for variant_size in v.sizes
                        ]
                        if v.sizes else None
                    ),
                    imagenes=(
                        [
                            UpdateImageCommand(
                                id=img.id,
                                owner_id=img.owner_id,
                                image_url=img.image_url,
                                public_id=img.public_id,
                                to_delete=img.to_delete
                            )
                            for img in v.imagenes
                        ]
                        if v.imagenes else None
                    ),
                    to_delete=v.to_delete,
                    temp_key=v.temp_key
                )
                for v in schema.variants
            ]

        return UpdateProductCommand(
            id=schema.id,
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            marca=schema.marca,
            categoria=schema.categoria,
            model_family=schema.model_family,
            fit=schema.fit,
            variants=product_variants,
            name_changed=schema.name_changed,
            temp_keys=schema.temp_keys
        )
    
    @staticmethod
    def to_filter_command(schema: FilterSchema) -> FilterProductCommand:
        colors = COLOR_FAMILY_MAP.get(schema.color)
        return FilterProductCommand(
            name=schema.name,
            marca=schema.marca,
            categoria=schema.categoria,
            model_family=schema.model_family,
            colors=colors,
            sizes=schema.sizes
        )
