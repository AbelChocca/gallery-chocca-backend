from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.media.protocol import CloudinaryProtocol
from app.infra.async_utils import AsyncProtocol
from app.core.app_exception import AppException

from app.domain.media.media_dto import MediaImageDTO

from typing import BinaryIO, List

class MediaService:
    def __init__(
            self,
            image_repo: PostgresImageRepository,
            cloudinary_service: CloudinaryProtocol,
            async_service: AsyncProtocol
        ):
        self._image_repo: PostgresImageRepository = image_repo
        self._cloudinary_service: CloudinaryProtocol = cloudinary_service
        self._async_service: AsyncProtocol = async_service

    async def move_images_to_trash(self, images_public_id: List[str]) -> List[dict]:
        semaphore = self._async_service.create_semaphore(5)
        tasks = [
            self._async_service.run_in_semaphore(
                semaphore,
                self._cloudinary_service.rename_resource,
                public_id,
                self._trash_public_id(public_id)
            )
            for public_id in images_public_id
        ]

        _, errors = await self._async_service.run_in_gather(*tasks, return_exceptions=True)

        return errors
    
    async def recover_images_from_trash(self, images_public_id: List[str]) -> List[dict]:
        semaphore = self._async_service.create_semaphore(5)
        tasks = [
            self._async_service.run_in_semaphore(
                semaphore,
                self._cloudinary_service.rename_resource,
                self._trash_public_id(public_id),
                public_id
            )
            for public_id in images_public_id
        ]

        _, errors = await self._async_service.run_in_gather(*tasks, return_exceptions=True)

        return errors
    
    async def move_image_to_trash(self, public_id: str) -> None:
        try:
            await self._async_service.run_blocking(
                self._cloudinary_service.rename_resource,
                public_id,
                self._trash_public_id(public_id)
            )
        except AppException as ae:
            ae["head_context"] = {
                "service": "media",
                "service_event": "move_image_to_trash"
            }

            raise ae
    async def recover_image_from_trash(self, public_id: str) -> None:
        try:
            await self._async_service.run_blocking(
                self._cloudinary_service.rename_resource,
                self._trash_public_id(public_id),
                public_id
            )
        except AppException as ae:
            ae["head_context"] = {
                "service": "media",
                "service_event": "move_image_to_trash"
            }

        
    async def upload_image(self, image_resource: BinaryIO, folder: str) -> MediaImageDTO:
        try:
            data = await self._async_service.run_blocking(
                self._cloudinary_service.upload_image,
                image_resource,
                folder
            )

            return data
        except AppException as ae:
            ae["head_context"] = {
                "service": "media",
                "service_event": "upload_image"
            }

            raise ae

    async def upload_images_batch(self, images_resource: List[BinaryIO], folder: str) -> List[MediaImageDTO]:
        semaphore = self._async_service.create_semaphore(3)
        tasks = [
            self._async_service.run_in_semaphore(
                semaphore,
                self._cloudinary_service.upload_image,
                file,
                folder=folder
            )
            for file in images_resource
        ]
        
        uploaded: List[MediaImageDTO] = []
        uploaded, errors = await self._async_service.run_in_gather(*tasks, return_exceptions=True)

        if errors:
            compesated_errors = await self.move_images_to_trash(uploaded)
            raise AppException(
                "Upload images batch failed",
                {
                    "errors": errors,
                    "uploaded_count": len(uploaded),
                    "failed_count": len(errors),
                    "compesated_errors": compesated_errors
                }
            )

        return uploaded

    def _trash_public_id(self, public_id: str) -> str:
        filename = public_id.rsplit("/", 1)[-1]
        return f"trash/{filename}"