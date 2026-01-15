from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository

from typing import List, Optional

class GetFavoriteProductsCase:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            favorites_repo: PostgresFavoritesRepository,
            ):
        self.product_repo: PostgresProductRepository =  product_repo
        self.favorites_repo: PostgresFavoritesRepository = favorites_repo


    async def execute(
            self, 
            session_id: Optional[int] = None,
            user_id: Optional[int] = None
            ):
        favorites_product_ids: List[int] = await self.favorites_repo.get_favorites_by_user_id(session_id)