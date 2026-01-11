from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.domain.media.protocol import MediaProtocol
from app.core.log.protocole import LoggerProtocol
from app.domain.cache.protocole import CacheProtocol

from app.domain.product.entities.product import Product

from typing import List

class DeleteProductCase:
    def __init__(
            self,
            repo: PostgresProductRepository,
            image_repo: PostgresImageRepository,
            media_service: MediaProtocol,
            cache_service: CacheProtocol,
            logger: LoggerProtocol
            ):
        self.repo: PostgresProductRepository = repo
        self.image_repo: PostgresImageRepository = image_repo
        self.media_service: MediaProtocol = media_service
        self.cache_service: CacheProtocol = cache_service
        self.logger: LoggerProtocol = logger

    async def execute(
            self,
            product_id: int
    ) -> None:
        product_to_delete: Product = await self.repo.get_by_id(product_id)

        # Cache invalidation
        await self.cache_service.cache_delete(Product.get_filter_key(id=product_to_delete.id))
        await self.cache_service.cache_delete(Product.get_filter_key(category=product_to_delete.categoria))
        await self.cache_service.cache_delete(Product.get_filter_key(brand=product_to_delete.marca, category=product_to_delete.categoria))

        # Del images from cloud service
        images_to_delete: List[str] = product_to_delete.get_all_variants_images_id()
        for image_id in images_to_delete:
            self.media_service.delete_image(image_id)
            await self.image_repo.delete_by_id(image_id)

        await self.repo.delete_by_id(product_id)
        self.logger.info(f"Product with id:{product_id} was deleted successfully")