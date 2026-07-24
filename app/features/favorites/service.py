from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.features.products.product import Product

from app.features.favorites.dto import FavoritesFilterDto
from app.features.favorites.favorite_entity import FavoriteEntity

class FavoriteService:
    def __init__(
            self,
            favorite_repo: PostgresFavoritesRepository,
        ):
        self._favorite_repo = favorite_repo

    async def delete_favorite_of_product(
        self,
        product_id: int,
    ) -> None:
        await self._favorite_repo.delete_favorite_of_product(
            product_id
        )

    async def get_favorites_by_user_id(
        self,
        filter: FavoritesFilterDto,
        offset: int,
        limit: int,
        user_id: int,
    ) -> list[Product]:

        return await self._favorite_repo.get_favorites_by_user_id(
            filter=filter,
            offset=offset,
            limit=limit,
            user_id=user_id
        )
    
    async def get_favorites_by_session_id(
        self,
        filter: FavoritesFilterDto,
        offset: int,
        limit: int,
        session_id: str,
    ) -> list[Product]:

        return await self._favorite_repo.get_favorites_by_session_id(
            filter=filter,
            offset=offset,
            limit=limit,
            session_id=session_id
        )
    
    async def count_favorites(
        self,
        *,
        user_id: int | None = None,
        session_id: str | None = None,
    ) -> int:

        return await self._favorite_repo.count_favorites(
            user_id=user_id,
            session_id=session_id
        )

    async def get_favorite_status(
        self,
        *,
        product_id: int,
        user_id: int | None = None,
        session_id: str | None = None
    ) -> dict:

        is_favorite: bool = (
            await self._favorite_repo.get_favorite_status(
                product_id=product_id,
                user_id=user_id,
                session_id=session_id
            )
        )

        return {
            "is_favorite": is_favorite
        }
    
    async def set_favorite_product(
        self,
        *,
        product_id: int,
        user_id: int | None = None,
        session_id: str | None = None
    ) -> dict:

        favorite = FavoriteEntity(
            product_id=product_id,
            user_id=user_id,
            session_id=session_id
        )

        await self._favorite_repo.save(favorite)

        return {
            "is_favorite": True
        }
        
    async def delete_favorite(
        self,
        *,
        product_id: int,
        user_id: int | None = None,
        session_id: str | None = None
    ) -> dict:

        if user_id is not None:
            await self._favorite_repo.delete_favorite_by_user_id(
                product_id,
                user_id
            )
        else:
            await self._favorite_repo.delete_favorite_by_session_id(
                product_id,
                session_id
            )

        return {
            "is_favorite": False
        }