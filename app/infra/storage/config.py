from cloudinary import config
from app.core.settings.pydantic_settings import settings

def init_cloudinary_client() -> None:
    config(
        cloud_name=settings.CLOUDINARY_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )