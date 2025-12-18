from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.dto.product_dto import ReadProductDTO, FilterSchemaDTO, UpdateProductDTO
from app.modules.product.domain.dto.variant_dto import ReadProductVariantDTO, UpdateProductVariantDTO
from app.modules.product.domain.dto.variant_image_dto import UpdateVariantImageDTO
from app.modules.product.domain.dto.variant_image_dto import ReadVariantImageDTO
from app.application.products.commands import FilterProductCommand, UpdateProductCommand

class ProductCommandToDTOMapper:
    @staticmethod
    def to_filter_dto(command: FilterProductCommand)-> FilterSchemaDTO:
        return FilterSchemaDTO(
            name=command.name,
            marca=command.marca,
            categoria=command.categoria,
            modelo=command.modelo,
            minPrice=command.minPrice,
            maxPrice=command.maxPrice,
            color=command.color,
            promocion=command.promocion
        )
    @staticmethod
    def to_update_dto(command: UpdateProductCommand) -> UpdateProductDTO:
        return UpdateProductDTO(
            nombre=command.nombre,
            descripcion=command.descripcion,
            marca=command.marca,
            categoria=command.categoria,
            modelo=command.modelo,
            precio=command.precio,
            descuento=command.descuento,
            promocion=command.promocion,
            variants=[
                UpdateProductVariantDTO(
                    id=variant.id,
                    color=variant.color,
                    tallas=variant.tallas,
                    to_delete=variant.to_delete,
                    imagenes=[
                        UpdateVariantImageDTO(
                            to_delete=image.to_delete,
                            cloudinary_id=image.cloudinary_id
                        )
                        for image in variant.imagenes
                    ]
                )
                for variant in command.variants
            ]
        )

class ProductEntityToDTOMapper:
    @staticmethod
    def to_read_dto(entity: Product) -> ReadProductDTO:
        return ReadProductDTO(
            id=entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            categoria=entity.categoria,
            marca=entity.marca,
            modelo=entity.modelo,
            precio=entity.precio,
            descuento=entity.descuento,
            slug=entity.slug,
            promocion=entity.promocion,
            variants=[
                ReadProductVariantDTO(
                    id=variant.id,
                    product_id=variant.product_id,
                    color=variant.color,
                    tallas=variant.tallas,
                    imagenes=[
                        ReadVariantImageDTO(
                            id=image.id,
                            variant_id=image.variant_id,
                            url=image.url,
                            cloudinary_id=image.cloudinary_id
                        )
                        for image in variant.imagenes
                    ]
                )
                for variant in entity.variants
            ]
        )