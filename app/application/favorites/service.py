from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.domain.product.entities.product import Product
from app.shared.services.pagination.pagination_service import PaginationService

from app.domain.favorites.dto import FavoritesFilter
from app.core.exceptions import ValidationError

class FavoriteService:
    def __init__(
            self,
            favorite_repo: PostgresFavoritesRepository,
            product_repo: PostgresProductRepository,
            pagination_service: PaginationService
        ):
        self._favorite_repo = favorite_repo
        self._product_repo = product_repo
        self._pagination_service = pagination_service

    async def get_favorite_products(
        self,
        filter: FavoritesFilter,
        page: int = 1,
        limit: int = 20,
        session_id: int | None = None,
        user_id: int | None = None
    ) -> dict:
        self._validate_owner_id(user_id, session_id, filter=filter)
        offset: int = self._pagination_service.get_offset(page, limit)
        if user_id is not None:
            favorites_product: list[Product] = await self._favorite_repo.get_favorites_by_user_id(
                filter=filter,
                offset=offset,
                limit=limit,
                user_id=user_id
                )
            total_favorites: int = await self._favorite_repo.count_favorites(user_id=user_id)
        else:
            favorites_product: list[Product] = await self._favorite_repo.get_favorites_by_session_id(
                filter=filter,
                offset=offset,
                limit=limit,
                session_id=session_id
                )
            total_favorites: int = await self._favorite_repo.count_favorites(session_id=session_id)

        total_pages: int = self._pagination_service.get_total_pages(total_favorites, limit)
        current_page: int = self._pagination_service.get_current_page(offset, limit)

        return {
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            },
            "products": [
                product
                for product in favorites_product
            ],
            "total_items": total_favorites
        }
    
        
    def _validate_owner_id(
        self,
        user_id: int | None = None,
        session_id: str | None = None,
        **kwargs
    ) -> None:
        if (user_id is None) == (session_id is None):
            raise ValidationError(
                "Provide either user_id or session_id, but not both",
                context={
                    "service": "favorites",
                    "user_id": user_id,
                    "session_id": session_id
                    **kwargs
                }
            )