from app.api.v1.media.media_router import router
from app.api.dependencies.media.case_depends import get_delete_image_case
from app.application.media.cases.delete_image import DeleteImageCase
from app.api.security.dependencies.sessions import get_admin_session

from fastapi import status, Depends, Path
from fastapi.concurrency import run_in_threadpool
from typing import Dict, Annotated

@router.delete(
    "/image/delete/{public_id:path}",
    tags=["image"],
    status_code=status.HTTP_200_OK,
    summary="Delete an image by his public id in cloudinary"
)
async def delete_image(
    public_id: Annotated[str, Path(title="service id of the image")],
    case: Annotated[DeleteImageCase, Depends(get_delete_image_case)],
    _: Annotated[None, Depends(get_admin_session)]
) -> Dict[str, str]:
    return await run_in_threadpool(case.execute, public_id)