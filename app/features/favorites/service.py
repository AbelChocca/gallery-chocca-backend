from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.features.products.entities.product import Product
from app.shared.pagination.pagination_service import PaginationService
from app.features.products.service import ProductService

from app.features.favorites.dto import FavoritesFilterDto
from app.core.exceptions import ValidationError
from app.features.favorites.favorite_entity import FavoriteEntity

class FavoriteService:
    def __init__(
            self,
            favorite_repo: PostgresFavoritesRepository,
            pagination_service: PaginationService,
            product_service: ProductService
        ):
        self._favorite_repo = favorite_repo
        self._product_service = product_service
        self._pagination_service = pagination_service

    async def get_favorite_products(
        self,
        filter: FavoritesFilterDto,
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

        enriched_products = (
            await self._product_service.enrich_products(
                favorites_product
            )
        )

        total_pages: int = self._pagination_service.get_total_pages(total_favorites, limit)
        current_page: int = self._pagination_service.get_current_page(offset, limit)

        return {
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            },
            "products": [
                product.to_dict
                for product in enriched_products
            ],
            "total_items": total_favorites
        }
    
    async def get_favorite_status(
        self,
        *,
        product_id: int,
        user_id: int | None = None,
        session_id: str | None = None
    ) -> dict:

        self._validate_owner_id(
            user_id=user_id,
            session_id=session_id,
            product_id=product_id
        )

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

        self._validate_owner_id(
            user_id=user_id,
            session_id=session_id,
            product_id=product_id
        )

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

        self._validate_owner_id(
            user_id=user_id,
            session_id=session_id,
            product_id=product_id
        )

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