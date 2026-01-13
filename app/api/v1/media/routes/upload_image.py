from app.api.v1.media.media_router import router
from app.api.schemas.media.media_schema import ReadImage
from app.api.schemas.media.schema_mapper import OutputSchemaMapper
from app.api.dependencies.media.case_depends import get_upload_image_case
from app.application.media.cases.upload_image import UploadImageCase
from app.api.security.dependencies.sessions import get_admin_session

from fastapi import status, Depends, UploadFile, Path, File
from fastapi.concurrency import run_in_threadpool
from typing import Annotated

@router.post(
    "/image/{folder}",
    tags=["image"],
    status_code=status.HTTP_200_OK,
    response_model=ReadImage,
    summary="Upload an image to cloudinary and get compress url"
)
async def upload_image(
    file: Annotated[UploadFile, File(...)],
    folder: Annotated[str, Path(title="service's folder of the image")],
    case: Annotated[UploadImageCase, Depends(get_upload_image_case)],
    _: Annotated[None, Depends(get_admin_session)]
) -> ReadImage:
    res = await run_in_threadpool(case.execute, file.file, folder)
    return OutputSchemaMapper.to_schema(res)