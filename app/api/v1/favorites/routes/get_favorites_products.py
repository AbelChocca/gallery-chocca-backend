from app.api.v1.favorites.favorites_router import router
from app.application.favorites.cases.get_favorite_products import GetFavoriteProductsCase

from app.api.schemas.products.schema import GetGridProductsResponse
from app.api.schemas.pagination import PaginationSchema
from app.api.dependencies.favorites.case_depends import get_favorites_products_case
from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession
from app.api.schemas.favorites.schema import FavoritesFilterSchema
from app.api.schemas.favorites.schema_mapper import FavoriteSchemaToMapper

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
    case: Annotated[GetFavoriteProductsCase, Depends(get_favorites_products_case)]
) -> GetGridProductsResponse:
    if owner.is_user:
        res = await case.execute(
            filter=FavoriteSchemaToMapper.filter_schema_to_dto(filter_body),
            page=pagination.page,
            limit=pagination.limit,
            user_id=owner.user_id
            )
        return GetGridProductsResponse(**res)
    
    res = await case.execute(
        filter=FavoriteSchemaToMapper.filter_schema_to_dto(filter_body),
        page=pagination.page,
        limit=pagination.limit,
        session_id=owner.session_id
        )
    return GetGridProductsResponse(**res)