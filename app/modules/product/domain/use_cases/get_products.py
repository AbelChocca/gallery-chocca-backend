from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.entities.product import Product
from app.shared.dto.product_dto import FilterSchemaDTO

from typing import List


class GetProductsCase:
    def __init__(
            self,
            repo: ProductRepository
            ):
        self.repo: ProductRepository = repo

    async def count_products(self, dto: FilterSchemaDTO) -> int:
        res = await self.repo.count_filtered_products(
            filter_dto=dto
        )
        return res

    async def execute(
         self,
         dto: FilterSchemaDTO,
         offset: int,
         limit: int,
    ) -> List[Product]:
        products = await self.repo.get_all(
            offset=offset,
            limit=limit,
            filter_dto=dto
        )

        return products