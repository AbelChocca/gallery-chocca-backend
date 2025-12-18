from app.api.dependencies.cloudinary.repo import get_cloudinary_repo
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.application.cloudinary.cases.upload_image import UploadImageCase
from app.application.cloudinary.cases.delete_image import DeleteImageCase

from fastapi import Depends

def get_upload_image_case(repo: CloudinaryRepository = Depends(get_cloudinary_repo)) -> UploadImageCase:
    return UploadImageCase(repo)

def get_delete_image_case(repo: CloudinaryRepository = Depends(get_cloudinary_repo)) -> DeleteImageCase:
    return DeleteImageCase(repo)