from fastapi import Depends

from app.features.favorites.service import FavoriteService
from app.features.favorites.use_cases.get_favorites_products import (
    GetFavoriteProductsUseCase,
)
from app.shared.enrichers.product_enricher import ProductEnricher
from app.shared.enrichers.dependency import get_product_enricher
from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.shared.pagination.pagination_service import (
    PaginationService,
    get_pagination_service,
)


def get_favorite_service(
    uow: UnitOfWork = Depends(get_uow),
) -> FavoriteService:
    return FavoriteService(
        favorite_repo=uow.favorites,
    )

def get_favorite_products_use_case(
    favorite_service: FavoriteService = Depends(get_favorite_service),
    pagination_service: PaginationService = Depends(get_pagination_service),
    product_enricher: ProductEnricher = Depends(get_product_enricher),
) -> GetFavoriteProductsUseCase:
    return GetFavoriteProductsUseCase(
        favorite_service=favorite_service,
        pagination_service=pagination_service,
        product_enricher=product_enricher,
    )