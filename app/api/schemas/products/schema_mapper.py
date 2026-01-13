from app.domain.product.dto.product_dto import ReadProductDTO
from app.api.schemas.products.schema import CreateProductSchema, ProductRead, FilterSchema, UpdateProductSchema, ProductVariantRead
from app.api.schemas.media.media_schema import ReadImage
from app.application.products.commands import PublishProductCommand, PublishProductVariantCommand, UpdateProductCommand, UpdateProductVariantCommand, FilterProductCommand
from app.application.media.commands import UpdateImageCommand


class InputSchemaMapper:
    @staticmethod
    def to_publish_command(schema: CreateProductSchema) -> PublishProductCommand:
        product_variants = [
            PublishProductVariantCommand(
                color=v.color,
                tallas=v.tallas,
            )
            for v in schema.variants
        ]

        return PublishProductCommand(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            marca=schema.marca,
            categoria=schema.categoria,
            modelo=schema.modelo, # O modelo → tipo si así quieres
            precio=schema.precio,
            descuento=schema.descuento or 0.0,
            promocion=schema.promocion or False,
            variants=product_variants,
            temp_variants_id=schema.temp_variants_id
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
                    tallas=v.tallas,
                    imagenes=(
                        [
                            UpdateImageCommand(
                                id=img.id,
                                owner_id=img.owner_id,
                                image_url=img.image_url,
                                service_id=img.service_id,
                                to_delete=img.to_delete
                            )
                            for img in v.imagenes
                        ]
                        if v.imagenes else None
                    ),
                    to_delete=v.to_delete
                )
                for v in schema.variants
            ]

        return UpdateProductCommand(
            id=schema.id,
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            marca=schema.marca,
            categoria=schema.categoria,
            modelo=schema.modelo,
            precio=schema.precio,
            descuento=schema.descuento,
            promocion=schema.promocion,
            variants=product_variants,
            name_changed=schema.name_changed
        )
    
    @staticmethod
    def to_filter_command(schema: FilterSchema) -> FilterProductCommand:
        return FilterProductCommand(
            name=schema.name,
            marca=schema.marca,
            categoria=schema.categoria,
            modelo=schema.modelo,
            color=schema.color,
            minPrice=schema.minPrice,
            maxPrice=schema.maxPrice,
            promocion=schema.promocion
        )


class OutputSchemaMapper:
    @staticmethod
    def to_read_schema(dto: ReadProductDTO) -> ProductRead:
        product_variants = [
            ProductVariantRead(
                id=v.id,
                product_id=v.product_id,
                color=v.color,
                tallas=v.tallas,
                imagenes=[
                    ReadImage(
                        image_url=img.image_url,
                        owner_type=img.owner_type,
                        service_id=img.service_id,
                        owner_id=img.owner_id,
                        id=img.id,
                        alt_text=img.alt_text
                    )
                    for img in v.imagenes
                ]
            )
            for v in dto.variants
        ]

        return ProductRead(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            marca=dto.marca,
            categoria=dto.categoria,
            modelo=dto.modelo,
            precio=dto.precio,
            slug=dto.slug,
            descuento=dto.descuento,
            promocion=dto.promocion,
            variants=product_variants
        )
