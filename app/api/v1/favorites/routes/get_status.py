from app.api.dependencies.favorites.case_depends import get_favorite_status_case
from app.api.v1.favorites.favorites_router import router
from app.api.schemas.favorites.schema import FavoriteStatusSchema

from app.application.favorites.cases.get_status import GetFavoriteStatusCase
from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession
from fastapi import Depends, status, Path
from typing import Annotated

@router.get(
    path='/{product_id}/status',
    response_model=FavoriteStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Get favorite status of an product"
)
async def get_status(
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    product_id: Annotated[int, Path(...)],
    case: Annotated[GetFavoriteStatusCase, Depends(get_favorite_status_case)]
) -> FavoriteStatusSchema:
    if owner.is_user:
        res = await case.execute(product_id=product_id, user_id=owner.user_id)
        return FavoriteStatusSchema(**res)

    res = await case.execute(product_id=product_id, session_id=owner.session_id)
    return FavoriteStatusSchema(**res)