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
            raise CloudinaryException(
                "Cloudinary upload failed.",
                {
                    "service": "cloudinary/infra",
                    "event": "upload_image",
                    "folder": folder
                }
                ) from e

    def delete_image(self, public_id: str) -> None:
        try:
            destroy(public_id, resource_type="image")
        except CloudinaryError as e:
            raise CloudinaryException(
                "Cloudinary delete failed",
                {
                    "service": "cloudinary/infra",
                    "event": "delete_image",
                    "public_id": public_id,
                }
            ) from e