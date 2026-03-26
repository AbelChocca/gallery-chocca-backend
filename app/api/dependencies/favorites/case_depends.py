from app.application.favorites.cases.get_favorite_products import GetFavoriteProductsCase
from app.application.favorites.cases.delete_favorite import DeleteFavoriteCase
from app.application.favorites.cases.get_status import GetFavoriteStatusCase
from app.application.favorites.cases.set_favorite import SetFavoriteProductCase
from app.application.products.service import ProductService
from app.application.favorites.service import FavoriteService

from app.infra.db.unit_of_work import UnitOfWork
from app.api.dependencies.uow import get_uow
from app.api.dependencies.products.service import get_product_service
from app.api.dependencies.favorites.service import get_favorite_service

from fastapi import Depends

def get_favorites_products_case(
    product_service: ProductService = Depends(get_product_service),
    favorite_service: FavoriteService = Depends(get_favorite_service)
) -> GetFavoriteProductsCase:
    return GetFavoriteProductsCase(
        favorite_service=favorite_service,
        product_service=product_service
    )

def get_delete_favorite_case(
    uow: UnitOfWork = Depends(get_uow)
) -> DeleteFavoriteCase:
    return DeleteFavoriteCase(
        favorite_repo=uow.favorites
    )

def get_favorite_status_case(
    uow: UnitOfWork = Depends(get_uow)
) -> GetFavoriteStatusCase:
    return GetFavoriteStatusCase(
        favorites_repo=uow.favorites
    )

def get_favorite_product_setter_case(
    uow: UnitOfWork = Depends(get_uow)
) -> SetFavoriteProductCase:
    return SetFavoriteProductCase(uow.favorites)
