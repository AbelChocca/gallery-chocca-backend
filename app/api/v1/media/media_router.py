from fastapi import APIRouter

router = APIRouter(prefix="/v1/media", tags=["media", "v1"])

from app.api.v1.media.routes import delete_image, upload_image