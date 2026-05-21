from app.features.favorites.favorites_router import router
from app.features.favorites.schema import FavoriteStatusSchema
from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession
from app.features.favorites.service import FavoriteService
from app.features.favorites.dependency import get_favorite_service

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
    service: Annotated[FavoriteService, Depends(get_favorite_service)]
) -> FavoriteStatusSchema:
    if owner.is_user:
        res = await service.set_favorite_product(product_id=product_id, user_id=owner.user_id)
        return FavoriteStatusSchema(**res)
    
    res = await service.set_favorite_product(product_id=product_id, session_id=owner.session_id)
    return FavoriteStatusSchema(**res)