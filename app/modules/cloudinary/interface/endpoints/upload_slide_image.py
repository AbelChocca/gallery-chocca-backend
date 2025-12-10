from app.modules.cloudinary.interface.cloudinary_router import router
from app.modules.cloudinary.interface.schema.cloudinary_schema import ReadImageSchema
from app.modules.cloudinary.interface.dependencies.case_depends import get_upload_image_case
from app.modules.cloudinary.interface.schema.schema_mapper import CloudinarySchemaMapper
from app.modules.cloudinary.domain.cases.upload_slide_image import UploadImageCase

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
    return CloudinarySchemaMapper.to_schema(res)