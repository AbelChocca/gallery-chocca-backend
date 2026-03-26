from app.api.dependencies.favorites.case_depends import get_favorite_product_setter_case
from app.api.v1.favorites.favorites_router import router
from app.api.schemas.favorites.schema import FavoriteStatusSchema
from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession
from app.application.favorites.cases.set_favorite import SetFavoriteProductCase

from fastapi import Depends, status, Path
from typing import Annotated

@router.post(
    "/{product_id}",
    response_model=FavoriteStatusSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Set a product to favorites"
)
async def set_favorite(
    product_id: Annotated[int, Path(...)],
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    case: Annotated[SetFavoriteProductCase, Depends(get_favorite_product_setter_case)]
) -> FavoriteStatusSchema:
    if owner.is_user:
        res = await case.execute(product_id=product_id, user_id=owner.user_id)
        return FavoriteStatusSchema(**res)
    
    res = await case.execute(product_id=product_id, session_id=owner.session_id)
    return FavoriteStatusSchema(**res)