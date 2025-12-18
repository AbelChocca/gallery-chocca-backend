from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.core.log.logger_repository import LoggerRepository
from app.modules.product.domain.dto.product_dto import ReadProductDTO
from app.application.products.commands import FilterProductCommand
from app.application.products.helper_mapper import ProductCommandToDTOMapper, ProductEntityToDTOMapper

from typing import List


class GetProductsCase:
    def __init__(
            self,
            repo: ProductRepository,
            logger: LoggerRepository
            ):
        self.repo: ProductRepository = repo
        self.logger: LoggerRepository = logger

    async def count_products(self, command: FilterProductCommand) -> int:
        res = await self.repo.count_filtered_products(
            filter_dto=ProductCommandToDTOMapper.to_filter_dto(command)
        )
        self.logger.info(f"Got it! total count products with filters: {res}")
        return res

    async def execute(
         self,
         command: FilterProductCommand,
         offset: int,
         limit: int,
    ) -> List[ReadProductDTO]:
        products = await self.repo.get_all(
            offset=offset,
            limit=limit,
            filter_dto=ProductCommandToDTOMapper.to_filter_dto(command)
        )
        self.logger.info("Products with filter was successfully get.")
        
        return [
            ProductEntityToDTOMapper.to_read_dto(product)
            for product in products
        ]