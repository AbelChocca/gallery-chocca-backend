from app.features.favorites.favorites_router import router

from app.features.products.schema import GetGridProductsResponse
from app.shared.pagination.schema import PaginationSchema
from app.features.favorites.service import FavoriteService
from app.features.favorites.dependency import get_favorite_service
from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession
from app.features.favorites.schema import FavoritesFilterSchema
from app.features.favorites.dto import FavoritesFilterDto


from fastapi import Depends, status
from typing import Annotated

@router.get(
    path="/",
    response_model=GetGridProductsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get your favorite products based on you user id or anon session id"
)
async def get_favorites_products(
    filter_body: Annotated[FavoritesFilterSchema, Depends()],
    pagination: Annotated[PaginationSchema, Depends()],
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[FavoriteService, Depends(get_favorite_service)]
) -> GetGridProductsResponse:
    if owner.is_user:
        res = await service.get_favorite_products(
            filter=FavoritesFilterDto(**filter_body.model_dump()),
            page=pagination.page,
            limit=pagination.limit,
            user_id=owner.user_id
            )
        return GetGridProductsResponse(**res)
    
    res = await service.get_favorite_products(
        filter=FavoritesFilterDto(**filter_body.model_dump()),
        page=pagination.page,
        limit=pagination.limit,
        session_id=owner.session_id
        )
    return GetGridProductsResponse(**res)