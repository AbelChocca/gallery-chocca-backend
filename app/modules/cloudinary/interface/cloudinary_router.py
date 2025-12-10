from fastapi import APIRouter

router = APIRouter(prefix="/cloudinary", tags=["cloudinary"])

from app.modules.cloudinary.interface.endpoints import delete_image, upload_slide_image