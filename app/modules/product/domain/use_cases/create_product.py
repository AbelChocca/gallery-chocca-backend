from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.core.log.repository_logger import LoggerRepository
from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.entities.variant_color import VariantColor
from app.modules.product.domain.entities.variant_image import VariantImage
from app.shared.dto.product_dto import ProductDTO
from app.shared.exceptions.domain.product_exception import (
    InvalidProductNameException, 
    InvalidDiscountPercentException, 
    MissingVariantsException
)
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException

class CreateProductUseCase:
    def __init__(
            self, 
            repo: ProductRepository,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.logger = logger

    async def execute(self, dto: ProductDTO) -> Product:
        try:
            product_variants = [
                VariantColor(
                    color=variant.color,
                    tallas=variant.tallas,
                    imagenes=[
                        VariantImage(
                            url=image.url,
                            cloudinary_id=image.cloudinary_id
                        )
                        for image in variant.imagenes
                    ]
                )
                for variant in (dto.variants or [])
            ]
            new_product = Product(
                nombre=dto.nombre,
                descripcion=dto.descripcion,
                precio=dto.precio,
                marca=dto.marca,
                categoria=dto.categoria,
                modelo=dto.modelo,
                descuento=dto.descuento,
                variants=product_variants,
                promocion=dto.promocion
            )

            return await self.repo.save(new_product)
        except (
            InvalidDiscountPercentException,
            InvalidProductNameException,
            MissingVariantsException
            ) as e:
            self.logger.warning(f"There was an error to create an product: {str(e)}")
            raise e
        except DatabaseException as e:
            self.logger.error(f"Database's internal error: {str(e)}")
            raise e