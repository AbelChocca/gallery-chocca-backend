from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.core.log.logger_repository import LoggerRepository
from app.modules.cache.cache_repository import CacheRepository

from app.modules.product.domain.entities.product import Product

from typing import List

class DeleteProductCase:
    def __init__(
            self,
            repo: ProductRepository,
            image_repo: CloudinaryRepository,
            cache_repo: CacheRepository,
            logger: LoggerRepository
            ):
        self.repo: ProductRepository = repo
        self.image_repo: CloudinaryRepository = image_repo
        self.cache_repo: CacheRepository = cache_repo
        self.logger: LoggerRepository = logger

    async def execute(
            self,
            product_id: int
    ) -> None:
        """
        Delete product from database and his variant's images from cloudinary service, by her id
        
        :param self: Default
        :param product_id: Product id
        :type product_id: int
        """
        product_to_delete: Product = await self.repo.get_by_id(product_id)

        # Cache invalidation
        await self.cache_repo.cache_delete(Product.get_filter_key(id=product_to_delete.id))
        await self.cache_repo.cache_delete(Product.get_filter_key(category=product_to_delete.categoria))

        # Del images from cloud service
        images_to_delete: List[str] = product_to_delete.get_all_variants_images_id()
        for image_id in images_to_delete:
            self.image_repo.delete_image(image_id)

        await self.repo.delete_by_id(product_id)
        self.logger.info(f"Product with id:{product_id} was deleted successfully")