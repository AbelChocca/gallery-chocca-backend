from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.dto.product_dto import ReadProductDTO
from app.core.log.logger_repository import LoggerRepository
from app.application.products.helper_mapper import ProductEntityToDTOMapper

class GetProductByIDCase:
    def __init__(
            self,
            repo: ProductRepository,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.logger = logger

    async def execute(self, product_id: int) -> ReadProductDTO:
        product = await self.repo.get_by_id(product_id)
        self.logger.info(f"Product with id:{product_id} was successfully get.")

        return ProductEntityToDTOMapper.to_read_dto(product)

