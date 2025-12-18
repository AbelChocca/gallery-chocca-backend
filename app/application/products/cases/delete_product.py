from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.core.log.logger_repository import LoggerRepository

class DeleteProductCase:
    def __init__(
            self,
            repo: ProductRepository,
            logger: LoggerRepository
            ):
        self.repo: ProductRepository = repo
        self.logger: LoggerRepository = logger

    async def execute(
            self,
            product_id: int
    ) -> None:
        await self.repo.delete_by_id(product_id)
        self.logger.info(f"Product with id:{product_id} was deleted successfully")