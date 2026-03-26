from app.api.dependencies.favorites.case_depends import get_delete_favorite_case
from app.api.schemas.favorites.schema import FavoriteStatusSchema
from app.application.favorites.cases.delete_favorite import DeleteFavoriteCase
from app.api.v1.favorites.favorites_router import router

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
    case: Annotated[DeleteFavoriteCase, Depends(get_delete_favorite_case)]
) -> FavoriteStatusSchema:
    if owner.is_user:
        res = await case.execute(
            product_id=product_id,
            user_id=owner.user_id
        )
        return FavoriteStatusSchema(**res)
    
    res = await case.execute(
        product_id=product_id,
        session_id=owner.session_id
    )
    return FavoriteStatusSchema(**res)