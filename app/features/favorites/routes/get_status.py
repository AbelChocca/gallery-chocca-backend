from app.features.favorites.favorites_router import router
from app.features.favorites.schema import FavoriteStatusSchema

from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession
from fastapi import Depends, status, Path
from typing import Annotated
from app.features.favorites.service import FavoriteService
from app.features.favorites.dependency import get_favorite_service

@router.get(
    path='/{product_id}/status',
    response_model=FavoriteStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Get favorite status of an product"
)
async def get_status(
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    product_id: Annotated[int, Path(...)],
    service: Annotated[FavoriteService, Depends(get_favorite_service)]
) -> FavoriteStatusSchema:
    if owner.is_user:
        res = await service.get_favorite_status(product_id=product_id, user_id=owner.user_id)
        return FavoriteStatusSchema(**res)

    res = await service.get_favorite_status(product_id=product_id, session_id=owner.session_id)
    return FavoriteStatusSchema(**res)