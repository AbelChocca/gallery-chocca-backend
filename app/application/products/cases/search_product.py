from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.dto.product_dto import ReadProductDTO
from app.application.products.helper_mapper import ProductEntityToDTOMapper

from typing import List

class SearchProductCase:
    def __init__(
            self,
            repo: ProductRepository
            ):
        self.repo = repo

    async def execute(self, query: str, offset: int = 0, limit: int = 3) -> List[ReadProductDTO]:
        products = await self.repo.search_related(query=query, offset=offset, limit=limit)

        return [
            ProductEntityToDTOMapper.to_read_dto(
                product
            )
            for product in products
        ]