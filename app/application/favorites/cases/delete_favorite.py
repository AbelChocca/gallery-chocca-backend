from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.core.exceptions import ValidationError

class DeleteFavoriteCase:
    def __init__(
            self,
            favorite_repo: PostgresFavoritesRepository
            ):
        self._favorite_repo = favorite_repo

    async def execute(
            self,
            *,
            product_id: int,
            user_id: int = None,
            session_id: str = None
            ) -> dict:
        if (user_id is None) == (session_id is None):
            raise ValidationError(
                "Provide either user_id or session_id, but not both",
                context={
                    "service": "favorites",
                    "user_id": user_id,
                    "session_id": session_id,
                    "product_id": product_id
                }
            )
        
        if user_id is not None:
            await self._favorite_repo.delete_favorite_by_user_id(product_id, user_id)
        else:
            await self._favorite_repo.delete_favorite_by_session_id(product_id, session_id)
            
        return {"is_favorite": False}