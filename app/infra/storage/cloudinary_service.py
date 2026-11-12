import hashlib
import hmac
import re


import cloudinary
from enum import Enum

from cloudinary.uploader import rename, upload, destroy, Error as CloudinaryError
from typing import BinaryIO

from app.infra.storage.protocol import StorageProtocol
from app.features.media.dto import MediaImageDTO
from app.infra.storage.exceptions import StorageException
from app.core.settings.pydantic_settings import settings


class CloudinaryService(StorageProtocol):
    def upload_image(self, file: BinaryIO, folder: str) -> MediaImageDTO:

        self._validate_cloudinary_config()
        if isinstance(folder, Enum):
            folder = folder.value

        try:
            result = upload(
                file,
                folder=folder,
                resource_type="image",
                format="webp",
            )
            optimized_url = result["secure_url"].replace("/upload/", "/upload/f_auto,q_auto/")
            return MediaImageDTO(
                url=optimized_url,
                public_id=result["public_id"]
            )
        
        except CloudinaryError as e:
            error_message = str(e)

            match = re.search(
                r"Invalid Signature ([a-f0-9]{40}).*?"
                r"timestamp=(\d+)",
                error_message,
            )

            signature_debug = None

            if match:
                rejected_signature = match.group(1)
                timestamp = match.group(2)

                string_to_sign = (
                    f"folder={folder}"
                    f"&format=webp"
                    f"&timestamp={timestamp}"
                )

                cfg = cloudinary.config()

                def matches_signature(secret: str | None) -> bool:
                    if not secret:
                        return False

                    calculated = hashlib.sha1(
                        (string_to_sign + secret).encode("utf-8")
                    ).hexdigest()

                    return hmac.compare_digest(
                        calculated,
                        rejected_signature,
                    )

                signature_debug = {
                    "sdk_signature_matches": matches_signature(
                        cfg.api_secret
                    ),
                    "settings_signature_matches": matches_signature(
                        settings.CLOUDINARY_API_SECRET
                    ),
                    "cloud_name_matches": (
                        cfg.cloud_name == settings.CLOUDINARY_NAME
                    ),
                    "api_key_matches": (
                        cfg.api_key == settings.CLOUDINARY_API_KEY
                    ),
                }

            raise StorageException(
                "Storage upload failed.",
                {
                    "service": "storage/infra",
                    "event": "upload_image",
                    "folder": folder,
                    "cloudinary_error": error_message,
                    "signature_debug": signature_debug,
                },
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

    @staticmethod
    def _validate_cloudinary_config() -> None:
        cfg = cloudinary.config()

        valid = (
            cfg.cloud_name == settings.CLOUDINARY_NAME
            and hmac.compare_digest(
                str(cfg.api_key or ""),
                str(settings.CLOUDINARY_API_KEY or ""),
            )
            and hmac.compare_digest(
                str(cfg.api_secret or ""),
                str(settings.CLOUDINARY_API_SECRET or ""),
            )
        )

        if not valid:
            raise StorageException(
                "Cloudinary configuration mismatch.",
                {
                    "service": "storage/infra",
                    "event": "validate_config",
                    "cloud_name": cfg.cloud_name,
                    "api_key_configured": bool(cfg.api_key),
                    "secret_configured": bool(cfg.api_secret),
                },
            )
        
def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()
