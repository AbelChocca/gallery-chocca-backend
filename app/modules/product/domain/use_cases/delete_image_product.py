from app.modules.product.domain.repositories.repository_product import ProductRepository

class DeleteImageProductCase:
    def __init__(
            self,
            repo: ProductRepository
            ):
        self.repo = repo


    async def execute(self, cloudinary_id: str) -> None:
        await self.repo.delete_image_by_id(cloudinary_id)
