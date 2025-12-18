from app.api.v1.cloudinary.cloudinary_router import router
from app.api.dependencies.cloudinary.case_depends import get_delete_image_case
from app.application.cloudinary.cases.delete_image import DeleteImageCase

from fastapi import status, Depends
from typing import Dict

@router.delete(
    "/delete/{public_id:path}",
    tags=["image"],
    status_code=status.HTTP_200_OK,
    summary="Delete an image by his public id in cloudinary"
)
def delete_image(
    public_id: str,
    case: DeleteImageCase = Depends(get_delete_image_case)
) -> Dict[str, str]:
    return case.execute(public_id)