from app.api.v1.cloudinary.cloudinary_router import router
from app.api.schemas.cloudinary.cloudinary_schema import ReadImageSchema
from app.api.schemas.cloudinary.schema_mapper import OutputSchemaMapper
from app.api.dependencies.cloudinary.case_depends import get_upload_image_case
from app.application.cloudinary.cases.upload_image import UploadImageCase

from fastapi import status, Depends, UploadFile

@router.post(
    "/image/{folder}",
    tags=["image"],
    status_code=status.HTTP_200_OK,
    response_model=ReadImageSchema,
    summary="Upload an image to cloudinary and get compress url"
)
def upload_image(
    file: UploadFile,
    folder: str,
    case: UploadImageCase = Depends(get_upload_image_case)
) -> ReadImageSchema:
    res = case.execute(file.file, folder)
    return OutputSchemaMapper.to_schema(res)