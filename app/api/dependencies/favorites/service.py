from app.application.favorites.service import FavoriteService

from app.shared.services.pagination.pagination_service import PaginationService, get_pagination_service
from app.api.dependencies.uow import get_uow
from app.infra.db.unit_of_work import UnitOfWork

from fastapi import Depends

def get_favorite_service(
        uow: UnitOfWork = Depends(get_uow),
        pagination_service: PaginationService = Depends(get_pagination_service)
) -> FavoriteService:
    return FavoriteService(
        favorite_repo=uow.favorites,
        product_repo=uow.products,
        pagination_service=pagination_service
    )