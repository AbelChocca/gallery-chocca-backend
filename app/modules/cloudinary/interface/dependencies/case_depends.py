from app.modules.cloudinary.interface.dependencies.repo import get_cloudinary_repo
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.modules.cloudinary.domain.cases.upload_slide_image import UploadImageCase
from app.modules.cloudinary.domain.cases.delete_image import DeleteImageCase

from fastapi import Depends

def get_upload_image_case(repo: CloudinaryRepository = Depends(get_cloudinary_repo)) -> UploadImageCase:
    return UploadImageCase(repo)

def get_delete_image_case(repo: CloudinaryRepository = Depends(get_cloudinary_repo)) -> DeleteImageCase:
    return DeleteImageCase(repo)