from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.domain.favorites.dto import FavoriteStatus

from typing import Optional

class DeleteFavoriteCase:
    def __init__(
            self,
            favorites_repo: PostgresFavoritesRepository
            ):
        self.favorites_repo = favorites_repo

    async def execute(
            self,
            product_id: int,
            user_id: Optional[int] = None,
            session_id: Optional[str] = None
            ) -> FavoriteStatus:
        if user_id:
            await self.favorites_repo.delete_favorite_by_user_id(product_id, user_id)
        else:
            await self.favorites_repo.delete_favorite_by_session_id(product_id, session_id)
            
        return FavoriteStatus(is_favorite=False)