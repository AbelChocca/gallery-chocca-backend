from app.features.favorites.service import FavoriteService

from app.shared.pagination.pagination_service import PaginationService, get_pagination_service
from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.products.dependency import get_product_service
from app.features.products.service import ProductService

from fastapi import Depends

def get_favorite_service(
        uow: UnitOfWork = Depends(get_uow),
        pagination_service: PaginationService = Depends(get_pagination_service),
        product_service: ProductService = Depends(get_product_service)
) -> FavoriteService:
    return FavoriteService(
        favorite_repo=uow.favorites,
        pagination_service=pagination_service,
        product_service=product_service
    )