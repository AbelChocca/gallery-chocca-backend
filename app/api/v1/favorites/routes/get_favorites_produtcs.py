from app.api.v1.favorites.favorites_router import router
from app.api.security.dependencies.sessions import get_user_id
from app.application.favorites.cases.get_favorite_products import GetFavoriteProducts

from app.api.schemas.products.schema import ProductRead

from fastapi import Depends, status
from typing import List, Annotated

@router.get(
    path="/",
    response_model=List[ProductRead],
    status_code=status.HTTP_200_OK,
    summary="Get your favorite products based on you user id or anon session id"
)
async def get_favorites_products(
    user_id: Annotated[int | None, Depends(get_user_id)],
    case: Annotated[GetFavoriteProducts, Depends]
) -> List[ProductRead]:
    if user_id:
        return 