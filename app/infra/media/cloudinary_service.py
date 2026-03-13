from app.infra.media.protocol import CloudinaryProtocol
from app.domain.media.media_dto import MediaImageDTO
from app.infra.media.exceptions import CloudinaryException

from cloudinary.uploader import rename, upload, destroy, Error as CloudinaryError
from typing import BinaryIO

class CloudinaryService(CloudinaryProtocol):
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
        
    def rename_resource(self, origin_public_id: str, destinatary_public_id: str) -> None:
        try:
            rename(
                origin_public_id,
                destinatary_public_id,
                overwrite=True
            )
        except CloudinaryError as e:
            raise CloudinaryException(
                "Cloudinary renamed failed",
                {
                    "service": "cloudinary/infra",
                    "event": "rename_resource",
                    "original_public_id": origin_public_id,
                    "destinaraty_public_id": destinatary_public_id
                }
            ) from e
        
def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()
