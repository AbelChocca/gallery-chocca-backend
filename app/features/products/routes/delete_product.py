from app.features.products.product_route import router
from app.api.security.resolvers.sessions import get_admin_session
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service

from fastapi import status, Depends, Path
from typing import Dict, Annotated

@router.delete(
    "/delete/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an product by her id"
)
async def delete_product(
    product_id: Annotated[int, Path(title="ID of the product to delete")],
    service: Annotated[ProductService, Depends(get_product_service)],
    _: Annotated[None, Depends(get_admin_session)]
) -> Dict[str, str]:
    await service.delete_product(product_id)
    return {"message": "Product was deleted successfully"}