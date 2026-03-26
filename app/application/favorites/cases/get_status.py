from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository

class GetFavoriteStatusCase:
    def __init__(
            self,
            favorites_repo: PostgresFavoritesRepository
            ):
        self.favorites_repo: PostgresFavoritesRepository = favorites_repo

    async def execute(
        self,
        *,
        product_id: int,
        user_id: int | None = None,
        session_id: str | None = None
    ) -> dict:
        is_favorite: bool = await self.favorites_repo.get_favorite_status(
            product_id=product_id,
            user_id=user_id,
            session_id=session_id
        )

        return {"is_favorite": is_favorite}