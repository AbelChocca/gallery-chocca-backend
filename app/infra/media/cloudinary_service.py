from app.domain.media.protocol import MediaProtocol
from app.domain.media.media_dto import MediaImageDTO
from app.infra.media.exceptions import CloudinaryException
from app.core.log.protocole import LoggerProtocol

from cloudinary.uploader import upload, destroy, Error as CloudinaryError
from typing import BinaryIO

class CloudinaryService(MediaProtocol):
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger

    def upload_image(self, file: BinaryIO, folder: str) -> MediaImageDTO:
        try:
            result = upload(file, folder=folder, resource_type="image", format="webp")
            optimized_url = result["secure_url"].replace("/upload/", "/upload/f_auto,q_auto/")
            return MediaImageDTO(
                url=optimized_url,
                public_id=result["public_id"]
            )
        except CloudinaryError as e:
            raise CloudinaryException(f"Cloudinary upload failed: {e}") from e

    def delete_image(self, public_id: str) -> None:
        try:
            return destroy(public_id, resource_type="image")
        except CloudinaryError as e:
            self.logger.error(f"Image with id: {public_id} wasn't deleted")
            raise CloudinaryException(f"Cloudinary delete failed: {e}") from e