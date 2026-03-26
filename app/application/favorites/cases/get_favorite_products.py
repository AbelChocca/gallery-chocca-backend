from app.application.products.service import ProductService
from app.application.favorites.service import FavoriteService

from app.domain.favorites.dto import FavoritesFilter

from typing import Any, Dict

class GetFavoriteProductsCase:
    def __init__(
            self,
            *,
            favorite_service: FavoriteService,
            product_service: ProductService
            ):
        self._favorite_service = favorite_service
        self._product_service = product_service

    async def execute(
            self, 
            *,
            filter: FavoritesFilter,
            page: int = 1,
            limit: int = 20,
            session_id: int | None = None,
            user_id: int | None = None
        ) -> Dict[str, Any]:
        favorite_products = await self._favorite_service.get_favorite_products(
            filter=filter,
            page=page,
            limit=limit,
            session_id=session_id,
            user_id=user_id
        )

        favorite_products["products"] = await self._product_service.enrich_products(favorite_products["products"])
        favorite_products["products"] = [product.to_dict for product in favorite_products["products"]]

        return favorite_products

