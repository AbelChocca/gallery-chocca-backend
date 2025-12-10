from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.core.log.repository_logger import LoggerRepository
from app.shared.dto.cloudinary_dto import CloudinaryImageDTO
from app.shared.exceptions.infra.infraestructure_exception import CloudinaryException

from cloudinary.uploader import upload, destroy, Error as CloudinaryError
from typing import IO

class InfraCloudinaryRepository(CloudinaryRepository):
    def __init__(self, logger: LoggerRepository):
        self.logger = logger
    def upload_image(self, file: IO[bytes], folder: str) -> CloudinaryImageDTO:
        """Uploads an image to Cloudinary."""
        try:
            result = upload(file, folder=folder, resource_type="image", format="webp")
            optimized_url = result["secure_url"].replace("/upload/", "/upload/f_auto,q_auto/")
            return CloudinaryImageDTO(
                url=optimized_url,
                public_id=result["public_id"]
            )
        except CloudinaryError as e:
            raise CloudinaryException(f"Cloudinary upload failed: {e}") from e

    def delete_image(self, public_id: str) -> None:
        """Deletes an image from Cloudinary."""
        try:
            return destroy(public_id, resource_type="image")
        except CloudinaryError as e:
            self.logger.error(f"Image with id: {public_id} wasn't deleted")
            raise CloudinaryException(f"Cloudinary delete failed: {e}") from e