from app.features.favorites.schema import FavoriteStatusSchema
from app.features.favorites.favorites_router import router
from app.features.favorites.service import FavoriteService
from app.features.favorites.dependency import get_favorite_service

from app.api.security.resolvers.session_owner import get_session_owner, OwnerSession

from fastapi import status, Depends, Path
from typing import Annotated

@router.delete(
    "/products/{product_id}",
    response_model=FavoriteStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Delete an favorite product by her product id"
)
async def delete_favorite(
    product_id: Annotated[int, Path(...)],
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[FavoriteService, Depends(get_favorite_service)]
) -> FavoriteStatusSchema:
    if owner.is_user:
        res = await service.delete_favorite(
            product_id=product_id,
            user_id=owner.user_id
        )
        return FavoriteStatusSchema(**res)
    
    res = await service.delete_favorite(
        product_id=product_id,
        session_id=owner.session_id
    )
    return FavoriteStatusSchema(**res)