from app.api.dependencies.products.case_depends import get_delete_image_by_id_case
from app.api.v1.products.product_route import router
from app.application.products.cases.delete_image_product import DeleteImageProductCase

from fastapi import status, Depends
from typing import Dict


@router.delete(
    "/variants/image/{public_id:path}",
    status_code=status.HTTP_200_OK,
    summary="Delete an Image Variant by her cloudinary_id"
)
async def delete_image_product(
    public_id: str,
    case: DeleteImageProductCase = Depends(get_delete_image_by_id_case)
)-> Dict[str, str]:
    await case.execute(public_id)
    return {"message": f"the image with id: {public_id} was deleted successfully."}

