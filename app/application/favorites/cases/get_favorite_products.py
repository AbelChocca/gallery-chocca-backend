from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository

from app.application.products.helper_mapper import ProductEntityToDTOMapper
from app.domain.product.dto.product_dto import ReadProductDTO

from typing import List, Optional

class GetFavoriteProductsCase:
    def __init__(
            self,
            *,
            product_repo: PostgresProductRepository,
            favorites_repo: PostgresFavoritesRepository,
            image_repo: PostgresImageRepository
            ):
        self.product_repo: PostgresProductRepository =  product_repo
        self.favorites_repo: PostgresFavoritesRepository = favorites_repo
        self.image_repo: PostgresImageRepository = image_repo

    async def execute(
            self, 
            *,
            session_id: Optional[int] = None,
            user_id: Optional[int] = None
        ) -> List[ReadProductDTO]:
        if user_id is not None:
            favorites_product_ids: List[int] = await self.favorites_repo.get_favorites_by_user_id(user_id)
        else:
            favorites_product_ids: List[int] = await self.favorites_repo.get_favorites_by_session_id(session_id)

        products = await self.product_repo.get_products_with_similar_ids(favorites_product_ids)
        variant_ids: List[int] = []
        for product in products:
            variant_ids.extend(product.get_variants_id())

        images = await self.image_repo.get_by_owners(
            owner_type="product_variant",
            owner_ids=variant_ids
        )
        images_by_owner_id = {image.owner_id: image for image in images}
        for product in products:
            product.sync_images_to_variants(images_by_owner_id)

        return [
            ProductEntityToDTOMapper.to_read_dto(product)
            for product in products
        ]

