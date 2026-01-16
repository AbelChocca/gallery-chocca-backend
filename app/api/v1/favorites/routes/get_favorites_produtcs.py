from app.api.v1.favorites.favorites_router import router
from app.application.favorites.cases.get_favorite_products import GetFavoriteProductsCase

from app.api.schemas.products.schema import ProductRead
from app.api.schemas.products.schema_mapper import OutputSchemaMapper
from app.api.dependencies.favorites.case_depends import get_favorites_products_case
from app.api.dependencies.favorites.resolvers.favortire_owner import get_favorite_owner, FavoriteOwner

from fastapi import Depends, status
from typing import List, Annotated

@router.get(
    path="/",
    response_model=List[ProductRead],
    status_code=status.HTTP_200_OK,
    summary="Get your favorite products based on you user id or anon session id"
)
async def get_favorites_products(
    owner: Annotated[FavoriteOwner, Depends(get_favorite_owner)],
    case: Annotated[GetFavoriteProductsCase, Depends(get_favorites_products_case)]
) -> List[ProductRead]:
    if owner.is_user:
        favorite_products = await case.execute(user_id=owner.user_id)
        return [
            OutputSchemaMapper.to_read_schema(product)
            for product in favorite_products
        ]
    
    favorite_products = await case.execute(session_id=owner.session_id)
    return [
            OutputSchemaMapper.to_read_schema(product)
            for product in favorite_products
        ]