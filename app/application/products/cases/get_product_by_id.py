from app.application.products.service import ProductService

from typing import Dict, Any

class GetProductByIDCase:
    def __init__(
            self,
            product_service: ProductService
            ):
        self._product_service: ProductService = product_service

    async def execute(self, product_id: int) -> Dict[str, Any]:
        return await self._product_service.get_product_by_id(product_id)

