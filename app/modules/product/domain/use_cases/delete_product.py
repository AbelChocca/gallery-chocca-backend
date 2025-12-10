from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.core.log.repository_logger import LoggerRepository
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException

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
        try:
            await self.repo.delete_by_id(product_id)
        except DatabaseException as e:
            self.logger.error(f"Database's internal error: {str(e)}")
            raise e