from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.core.log.repository_logger import LoggerRepository
from app.shared.dto.product_dto import UpdateProductDTO
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException

from dataclasses import asdict

class UpdateProductCase:
    def __init__(
            self,
            repo: ProductRepository,
            logger: LoggerRepository
            ):
        self.repo: ProductRepository = repo
        self.logger: LoggerRepository = logger

    async def execute(
            self,
            dto: UpdateProductDTO,
            product_id: int
    ) -> Product:
        try:
            self.logger.info(f"Imprimiendo dto inicial: {asdict(dto)}")
            existing_product = await self.repo.get_by_id(product_id)

            existing_product.update_product(dto)
            self.logger.info(f"Imagenes de variantes despues de actualizar: ")
            for variant in existing_product.variants:
                for imagenes in variant.imagenes:
                    self.logger.info(vars(imagenes))

            new_product = await self.repo.save(existing_product)
            return new_product
        except DatabaseException as e:
            self.logger.error(f"Database's internal error: {str(e)}")
            raise e