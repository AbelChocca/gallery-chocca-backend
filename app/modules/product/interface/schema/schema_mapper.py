from app.shared.dto.product_dto import ProductDTO, FilterSchemaDTO, UpdateProductColorVariantDTO, UpdateProductDTO
from app.shared.dto.color_variant_dto import ColorVariantDTO, VariantImageDTO, UpdateVariantImageDTO, UpdateProductColorVariantDTO
from app.modules.product.interface.schema.schema import CreateProductSchema, ProductRead, FilterSchema, UpdateProductSchema, ProductVariantRead, VariantImageRead

from app.modules.product.domain.entities.product import Product


class ProductSchemaMapper:
    @staticmethod
    def to_create_dto(schema: CreateProductSchema) -> ProductDTO:
        product_variants = [
            ColorVariantDTO(
                color=v.color,
                tallas=v.tallas,
                imagenes=[
                    VariantImageDTO(
                        url=img.url,
                        cloudinary_id=img.cloudinary_id
                    )
                    for img in v.imagenes
                ]
            )
            for v in schema.variants
        ]

        return ProductDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            marca=schema.marca,
            categoria=schema.categoria,
            modelo=schema.modelo,          # O modelo → tipo si así quieres
            precio=schema.precio,
            descuento=schema.descuento or 0.0,
            promocion=schema.promocion or False,
            variants=product_variants
        )
    @staticmethod
    def to_update_dto(schema: UpdateProductSchema) -> UpdateProductDTO:
        product_variants = None

        if schema.variants:
            product_variants = [
                UpdateProductColorVariantDTO(
                    id=v.id,
                    product_id=v.product_id,
                    color=v.color,
                    tallas=v.tallas,
                    imagenes=(
                        [
                            UpdateVariantImageDTO(
                                id=img.id,
                                variant_id=img.variant_id,
                                url=img.url,
                                cloudinary_id=img.cloudinary_id
                            )
                            for img in v.imagenes
                        ]
                        if v.imagenes else None
                    )
                )
                for v in schema.variants
            ]

        return UpdateProductDTO(
            id=schema.id,
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            marca=schema.marca,
            categoria=schema.categoria,
            modelo=schema.modelo,
            precio=schema.precio,
            descuento=schema.descuento,
            promocion=schema.promocion,
            variants=product_variants
        )

    # ---------------------------------------------------------
    # FILTER
    # ---------------------------------------------------------
    @staticmethod
    def to_filter_dto(schema: FilterSchema) -> FilterSchemaDTO:
        return FilterSchemaDTO(
            name=schema.name,
            marca=schema.marca,
            categoria=schema.categoria,
            modelo=schema.modelo,
            color=schema.color,
            minPrice=schema.minPrice,
            maxPrice=schema.maxPrice,
            promocion=schema.promocion
        )

    # ---------------------------------------------------------
    # ENTITY TO READ SCHEMA
    # ---------------------------------------------------------
    @staticmethod
    def entity_to_schema(entity: Product) -> ProductRead:
        product_variants = [
            ProductVariantRead(
                id=v.id,
                product_id=v.product_id,
                color=v.color,
                tallas=v.tallas,
                imagenes=[
                    VariantImageRead(
                        id=img.id,
                        variant_id=img.variant_id,
                        url=img.url,
                        cloudinary_id=img.cloudinary_id
                    )
                    for img in v.imagenes
                ]
            )
            for v in entity.variants
        ]

        return ProductRead(
            id=entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            marca=entity.marca,
            categoria=entity.categoria,
            modelo=entity.modelo,
            precio=entity.precio,
            slug=entity.slug,
            descuento=entity.descuento,
            promocion=entity.promocion,
            variants=product_variants
        )
