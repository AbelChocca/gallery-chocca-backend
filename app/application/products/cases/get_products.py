from app.application.products.service import ProductService
from app.domain.product.dto.product_dto import FilterProductCommand

from typing import Dict, Any

class GetProductsCase:
    def __init__(
            self,
            product_service: ProductService
            ):
        self._product_service = product_service

    async def execute(
        self,
        command: FilterProductCommand,
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        return await self._product_service.get_products(
            command,
            page,
            limit
        )