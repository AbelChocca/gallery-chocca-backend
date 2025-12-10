from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.entities.product import Product

class GetProductByIDCase:
    def __init__(
            self,
            repo: ProductRepository
            ):
        self.repo = repo

    async def execute(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id)

        return product

