from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository

from app.domain.favorites.favorite_entity import FavoriteEntity
from typing import Optional

class SetFavoriteProductCase:
    def __init__(
            self,
            favorites_repo: PostgresFavoritesRepository
            ):
        self.favorites_repo = favorites_repo

    async def execute(
            self, 
            *,
            product_id: int,
            user_id: Optional[int] = None,
            session_id: Optional[str] = None
        ) -> dict:
        favorite = FavoriteEntity(
            product_id=product_id,
            user_id=user_id,
            session_id=session_id
        )

        await self.favorites_repo.save(favorite)

        return {"is_favorite": True}