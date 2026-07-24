from app.features.products.product_route import router
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission
from app.features.products.dependency import get_delete_product_use_case
from app.features.products.use_cases.delete_product import DeleteProductUseCase

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
    use_case: Annotated[DeleteProductUseCase, Depends(get_delete_product_use_case)]
) -> Dict[str, str]:
    await use_case.execute(product_id)
    return {"message": "Product was deleted successfully"}