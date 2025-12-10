from app.modules.cloudinary.interface.cloudinary_router import router
from app.modules.cloudinary.interface.dependencies.case_depends import get_delete_image_case
from app.modules.cloudinary.domain.cases.delete_image import DeleteImageCase

from fastapi import status, Depends
from typing import Dict

@router.delete(
    "/{public_id:path}",
    tags=["image"],
    status_code=status.HTTP_200_OK,
    summary="Delete an image by his public id in cloudinary"
)
def delete_image(
    public_id: str,
    case: DeleteImageCase = Depends(get_delete_image_case)
) -> Dict[str, str]:
    return case.execute(public_id)