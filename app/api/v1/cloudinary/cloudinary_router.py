from fastapi import APIRouter

router = APIRouter(prefix="/v1/cloudinary", tags=["cloudinary", "v1"])

from app.api.v1.cloudinary.routes import delete_image, upload_image