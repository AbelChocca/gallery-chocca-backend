from app.modules.product.interface.product_route import router
from app.modules.product.interface.dependencies.case_depends import get_delete_variant_by_id
from app.modules.product.domain.use_cases.delete_variant_product import DeleteProductVariantCase

from fastapi import status, Depends
from typing import Dict

@router.delete(
    "/variants/{variant_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product's variant by her id"
)
async def delete_variant_product(
    variant_id: int,
    case: DeleteProductVariantCase = Depends(get_delete_variant_by_id)
) -> Dict[str, str]:
    return await case.execute(variant_id)