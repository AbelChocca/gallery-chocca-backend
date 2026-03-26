from app.application.products.service import ProductService

from typing import List, Dict, Any

class SearchProductCase:
    def __init__(
            self,
            product_service: ProductService
            ):
        self.product_service = product_service

    async def execute(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        products = await self.product_service.get_products_related(query, limit)

        return [
            product.to_dict
            for product in products
        ]