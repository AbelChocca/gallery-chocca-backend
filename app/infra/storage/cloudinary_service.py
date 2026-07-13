from app.infra.storage.protocol import StorageProtocol
from app.features.media.dto import MediaImageDTO
from app.infra.storage.exceptions import StorageException

from cloudinary.uploader import rename, upload, destroy, Error as CloudinaryError
from typing import BinaryIO

class CloudinaryService(StorageProtocol):
    def upload_image(self, file: BinaryIO, folder: str) -> MediaImageDTO:
        try:
            result = upload(file, folder=folder, resource_type="image", format="webp")
            optimized_url = result["secure_url"].replace("/upload/", "/upload/f_auto,q_auto/")
            return MediaImageDTO(
                url=optimized_url,
                public_id=result["public_id"]
            )
        except CloudinaryError as e:
            raise StorageException(
                "Storage upload failed.",
                {
                    "service": "storage/infra",
                    "event": "upload_image",
                    "folder": folder,
                    "cloudinary_error": str(e),
                }
                ) from e

    def delete_image(self, public_id: str) -> None:
        try:
            destroy(public_id, resource_type="image")
        except CloudinaryError as e:
            raise StorageException(
                "Storage delete failed",
                {
                    "service": "storage/infra",
                    "event": "delete_image",
                    "public_id": public_id,
                    "cloudinary_error": str(e),
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
            raise StorageException(
                "Cloudinary renamed failed",
                {
                    "service": "storage/infra",
                    "event": "rename_resource",
                    "original_public_id": origin_public_id,
                    "destinaraty_public_id": destinatary_public_id,
                    "cloudinary_error": str(e),
                }
            ) from e
        
def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()
