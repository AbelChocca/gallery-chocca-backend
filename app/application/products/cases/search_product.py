from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.domain.product.dto.product_dto import ReadProductDTO
from app.application.products.helper_mapper import ProductEntityToDTOMapper

from typing import List

class SearchProductCase:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            image_repo: PostgresImageRepository
            ):
        self.product_repo = product_repo
        self.image_repo = image_repo

    async def execute(self, query: str, offset: int = 0, limit: int = 3) -> List[ReadProductDTO]:
        products = await self.product_repo.search_related(query=query, offset=offset, limit=limit)

        variants_id: List[int] = []
        for product in products:
            variants_id.extend(product.get_variants_id())

        images = await self.image_repo.get_images(
            owner_type="product_variant",
            owners_id=variants_id
        )

        for product in products:
            product.sync_images_to_variants(images)


        return [
            ProductEntityToDTOMapper.to_read_dto(
                product
            )
            for product in products
        ]