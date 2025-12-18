from app.modules.product.domain.repositories.repository_product import ProductRepository

from typing import Dict

class DeleteProductVariantCase:
    def __init__(
            self,
            repo: ProductRepository
            ):
        self.repo = repo


    async def execute(
        self, variant_id: int
    ) -> Dict[str, str]:
        await self.repo.delete_variant_by_id(variant_id)
        return {"message": "The variant was deleted successfully"}