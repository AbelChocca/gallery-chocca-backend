from app.features.products.product_route import router
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Path
from typing import Dict, Annotated

@router.delete(
    "/delete/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an product by her id",
    dependencies=[
        require_permission(Permission.PRODUCT_DELETE)
    ]
)
async def delete_product(
    product_id: Annotated[int, Path(title="ID of the product to delete")],
    service: Annotated[ProductService, Depends(get_product_service)]
) -> Dict[str, str]:
    await service.delete_product(product_id)
    return {"message": "Product was deleted successfully"}