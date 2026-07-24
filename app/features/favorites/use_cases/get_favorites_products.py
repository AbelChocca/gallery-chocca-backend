from app.features.favorites.service import FavoriteService
from app.shared.pagination.pagination_service import PaginationService
from app.shared.enrichers.product_enricher import ProductEnricher
from app.features.products.product_dto import CatalogProductDTO
from app.features.favorites.dto import FavoritesFilterDto

class GetFavoriteProductsUseCase:

    def __init__(
        self,
        favorite_service: FavoriteService,
        pagination_service: PaginationService,
        product_enricher: ProductEnricher,
    ):
        self._favorite_service = favorite_service
        self._pagination_service = pagination_service
        self._product_enricher = product_enricher

    async def execute(
        self,
        filter: FavoritesFilterDto,
        page: int = 1,
        limit: int = 20,
        session_id: str | None = None,
        user_id: int | None = None,
    ) -> CatalogProductDTO:
        
        offset = self._pagination_service.get_offset(
            page,
            limit
        )


        if user_id is not None:

            products = await self._favorite_service.get_favorites_by_user_id(
                filter,
                offset,
                limit,
                user_id
            )

            total = await self._favorite_service.count_favorites(
                user_id=user_id
            )

        else:

            products = await self._favorite_service.get_favorites_by_session_id(
                filter,
                offset,
                limit,
                session_id
            )

            total = await self._favorite_service.count_favorites(
                session_id=session_id
            )


        await self._product_enricher.attach_variant_images(
            products
        )


        return CatalogProductDTO.create(
            items=products,
            total_items=total,
            current_page=self._pagination_service.get_current_page(
                offset,
                limit
            ),
            total_pages=self._pagination_service.get_total_pages(
                total,
                limit
            ),
        )