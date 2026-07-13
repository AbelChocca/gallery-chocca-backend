from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.storage.protocol import StorageProtocol
from app.infra.async_utils import AsyncProtocol
from app.core.app_exception import AppException
from app.infra.saga.saga_service import SagaService
from app.features.media.types import ImageType
from app.features.media.entities.image import ImageEntity

from app.features.media.dto import MediaImageDTO
from app.features.media.entities.image import ImageEntity

from typing import BinaryIO, List

class MediaService:
    def __init__(
            self,
            image_repo: PostgresImageRepository,
            storage_service: StorageProtocol,
            async_service: AsyncProtocol,
            saga_service: SagaService
        ):
        self._image_repo: PostgresImageRepository = image_repo
        self._storage_service: StorageProtocol = storage_service
        self._async_service: AsyncProtocol = async_service
        self._saga_service: SagaService = saga_service

    async def get_images_by_owner_ids(
        self,
        *,
        owner_type: ImageType,
        owner_ids: list[int]
    ) -> list[ImageEntity]:
        
        if not owner_ids:
            return []

        return await self._image_repo.get_by_owners(
            owner_type=owner_type,
            owner_ids=owner_ids
        )
    
    async def get_first_image_by_owner(
        self,
        *,
        owner_type: ImageType,
        owner_id: int
    ) -> ImageEntity | None:
        return await self._image_repo.get_first_by_owner(
            owner_type=owner_type,
            owner_id=owner_id
        )
    
    async def delete_image_v2(
            self,
            image_public_id: str
    ) -> None:
        await self._image_repo.delete_by_id(image_public_id)

    
    # LEGACY
    async def delete_image(
        self, 
        image_public_id: str,
        saga_service: SagaService | None = None,
        ) -> None:
        await self._image_repo.delete_by_id(image_public_id)

        saga_service.add_step(
            action=self.move_image_to_trash,
            action_kwargs={
                "public_id": image_public_id
            },
            compensation=self.recover_image_from_trash,
            compensation_kwargs={
                "public_id": image_public_id
            },
            action_name=self.move_image_to_trash.__name__,
            compensation_name=self.recover_image_from_trash.__name__
        )

        return None
    
    async def delete_images(
        self,
        owner_type: str,
        images_public_id: list[str],
        saga_service: SagaService | None = None
    ) -> None:

        await self._image_repo.delete_many_images_by_publics_id(
            owner_type,
            images_public_id
        )

        if saga_service is not None:
            saga_service.add_step(
                action=self.move_images_to_trash,
                action_name=self.move_images_to_trash.__name__,
                compensation=self.recover_images_from_trash,
                compensation_name=self.recover_images_from_trash.__name__,
                action_kwargs={
                    "images_public_id": images_public_id
                },
                compensation_kwargs={
                    "images_public_id": images_public_id
                }
            )

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
                self._storage_service.rename_resource,
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
                self._storage_service.rename_resource,
                public_id,
                self._trash_public_id(public_id)
            )
        except AppException as ae:
            ae.context["head_context"] = {
                "service": "media",
                "service_event": "move_image_to_trash"
            }

            raise ae
    async def recover_image_from_trash(self, public_id: str) -> None:
        try:
            await self._async_service.run_blocking(
                self._storage_service.rename_resource,
                self._trash_public_id(public_id),
                public_id
            )
        except AppException as ae:
            ae.context["head_context"] = {
                "service": "media",
                "service_event": "move_image_to_trash"
            }

        
    async def upload_image(self, image_resource: BinaryIO, folder: str) -> MediaImageDTO:
        try:
            data = await self._async_service.run_blocking(
                self._storage_service.upload_image,
                image_resource,
                folder
            )

            return data
        except AppException as ae:
            ae.context["head_context"] = {
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
    
    async def create_image_batch(
            self,
            image_resources: list[BinaryIO],
            folder: str,
            owner_id: int,
            owner_type: str,
            saga_service: SagaService
    ) -> None:
        for image in image_resources:
            await self.create_image(
                image_resource=image,
                folder=folder,
                owner_id=owner_id,
                owner_type=owner_type,
                saga_service=saga_service
            )
    
    # LEGACY
    async def create_image(
            self,
            image_resource: BinaryIO,
            folder: str,
            owner_id: int,
            owner_type: str,
            saga_service: SagaService
    ) -> None:
        try:
            saga_service.add_step(
                action=self.upload_image,
                action_name=self.upload_image.__name__,
                action_kwargs={
                    "image_resource": image_resource,
                    "folder": folder
                }
            )

            storage_image: MediaImageDTO = await saga_service.execute_last()

            saga_service.set_last_step_compensation(
                compesation=self.recover_image_from_trash,
                compensation_name=self.recover_image_from_trash.__name__,
                compensation_kwargs={
                    "public_id": storage_image.public_id
                }
            )

            new_image = ImageEntity(
                image_url=storage_image.url,
                owner_type=owner_type,
                owner_id=owner_id,
                public_id=storage_image.public_id,
            )

            await self._image_repo.save(new_image, flush=False)
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae
        
    async def create_image_v2(
        self,
        image_url: str,
        public_id: str,
        owner_id: int,
        owner_type: str
    ) -> ImageEntity:
        new_image = ImageEntity(
            image_url=image_url,
            owner_type=owner_type,
            owner_id=owner_id,
            public_id=public_id,
        )

        await self._image_repo.save(
            new_image,
            flush=False
        )

        return new_image
    
    async def update_image(
        self,
        *,
        image: ImageEntity,
        image_url: str,
        public_id: str,
        is_primary: bool | None = None
    ) -> ImageEntity:
        image.image_url = image_url
        image.public_id = public_id

        if is_primary is not None:
            image.is_primary = is_primary

        return await self._image_repo.update(image)

    def _trash_public_id(self, public_id: str) -> str:
        filename = public_id.rsplit("/", 1)[-1]
        return f"trash/{filename}"