from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.repositories.sqlmodel_slide_repository import PostgresSlideRepository
from app.shared.services.cache_strategy.cache_strategy_service import CacheStrategyService
from app.shared.services.pagination.pagination_service import PaginationService
from app.infra.saga_service import SagaService
from app.infra.cache.protocole import CacheProtocol
from app.domain.slide.slide_dto import UpdateSlideCommand, UpdateSlidesOrder, SlideFiltersCommand, PublishSlideCommand
from app.domain.media.media_dto import MediaImageDTO
from app.domain.media.entities.image import ImageEntity

from app.domain.slide.slide_entity import SlideEntity
from app.core.exceptions import ValueNotFound

from typing import Callable, Awaitable, Any, BinaryIO

class SlideService:
    def __init__(
            self,
            slide_repo: PostgresSlideRepository,
            image_repo: PostgresImageRepository,
            pagination_service: PaginationService,
            cache_service: CacheProtocol,
            cache_strategy: CacheStrategyService,
        ):
        self._cache_service = cache_service
        self._cache_strategy = cache_strategy
        self._pagination_service = pagination_service
        self._slide_repo = slide_repo
        self._image_repo = image_repo

    
    async def get_by_id(self, slide_id: int) -> SlideEntity:
        slide = await self._slide_repo.get_by_id(slide_id)
        images = await self._image_repo.get_by_owner(
            owner_type="slide",
            owner_id=slide.id
        )
        if not images:
            raise ValueNotFound(
                "No images found for slide",
                {
                    "event": "delete_slide/execute",
                    "slide_id": slide_id
                }
            )
        slide.image = images[0]

        return slide
    
    async def delete_image(
            self, 
            image_public_id: str,
            saga_service: SagaService,
            action_func: Callable[..., Awaitable[Any] | Any],
            compensation_func: Callable[..., Awaitable[Any] | Any]
            ) -> None:
        await self._image_repo.delete_by_id(image_public_id)

        saga_service.add_step(
            action=action_func,
            action_kwargs={
                "public_id": image_public_id
            },
            compensation=compensation_func,
            compensation_kwargs={
                "public_id": image_public_id
            },
            action_name=action_func.__name__,
            compensation_name=compensation_func.__name__
        )

        return None
        
    async def update_slide(
        self,
        slide: SlideEntity,
        command: UpdateSlideCommand,
        new_image_file: BinaryIO,
        saga_service: SagaService,
        action_func: Callable[..., Awaitable[Any] | Any],
        compensation_func: Callable[..., Awaitable[Any] | Any]
    ) -> None:
        if slide.is_inactive and command.activo:
            slide.orden = await self._get_last_order()

        slide.update_slide(command.to_dict)

        if new_image_file is not None:
            saga_service.add_step(
                action=action_func,
                action_name=action_func.__name__,
                action_kwargs={
                    "image_resource": new_image_file,
                    "folder": "slides"
                }
            )
            cloud_image: MediaImageDTO = await saga_service.execute_last()
            saga_service.set_last_step_compensation(
                compesation=compensation_func,
                compensation_name=compensation_func.__name__,
                compensation_kwargs={
                    "public_id": cloud_image.public_id
                }
            )
            await self._image_repo.save(
                ImageEntity(
                    image_url=cloud_image.url,
                    owner_id=slide.id,
                    service_id=cloud_image.public_id,
                    owner_type="slide"
                )
            )

        await self._slide_repo.save(slide)

        await self._invalidate_slides()

    async def update_orders(
            self,
            command: UpdateSlidesOrder
    ) -> None:
        updates = [slide.to_dict for slide in command.slides]

        await self._slide_repo.update_many_orders(command.ids, updates)

        await self._invalidate_slides()

    async def get_slides(
        self,
        page: int, 
        limit:int, 
        filters_command: SlideFiltersCommand
    ) -> dict[str, Any]:
        offset: int = self._pagination_service.get_offset(page, limit)

        total_slides: int = await self._slide_repo.count_all(filters_command)

        total_pages: int = self._pagination_service.get_total_pages(total_slides, limit)
        current_page: int = self._pagination_service.get_current_page(offset, limit)

        cache_args = self._cache_strategy.operation_list("slides", { "filters": filters_command.to_dict, "page": page, "limit": limit})
        ttl = self._cache_strategy.determinate_ttl(cache_args)
        key = self._cache_strategy.generate_key(cache_args)

        return await self._cache_service.get_or_set_with_lock(
            key,
            ttl,
            callback=self._get_slides_data,
            kwargs={
                "command_filters": filters_command,
                "offset": offset,
                "limit": limit,
                "total_pages": total_pages,
                "current_page": current_page
            }
        )
    
    async def create_slide(
        self,
        command: PublishSlideCommand,
        image_file: BinaryIO,
        saga_service: SagaService,
        action_func: Callable[..., Awaitable[Any] | Any],
        compensation_func: Callable[..., Awaitable[Any] | Any]
    ) -> None:
        slide = SlideEntity(
            enlace_boton=command.enlace_boton,
            activo=command.activo,
        )
        if slide.activo:
            slide.orden = await self._get_last_order()

        slide = await self._slide_repo.save(slide)

        saga_service.add_step(
            action=action_func,
            action_name=action_func.__name__,
            action_kwargs={
                "image_resource": image_file,
                "folder": "slides"
            }
        )
        cloud_image: MediaImageDTO = await saga_service.execute_last()
        saga_service.set_last_step_compensation(
            compesation=compensation_func,
            compensation_name=compensation_func.__name__,
            compensation_kwargs={
                "public_id": cloud_image.public_id
            }
        )
        await self._image_repo.save(
            ImageEntity(
                image_url=cloud_image.url,
                owner_type="slide",
                owner_id=slide.id,
                public_id=cloud_image.public_id,
            )
        )

        await self._invalidate_slides()

    async def delete_slide(
            self,
            slide_id: int,
            saga_service: SagaService,
            action_func: Callable[..., Awaitable[Any] | Any],
            compensation_func: Callable[..., Awaitable[Any] | Any]
    ) -> dict:
        images = await self._image_repo.get_by_owner(
            owner_type="slide",
            owner_id=slide_id
        )
        if not images:
            raise ValueNotFound(
                "No images found for slide",
                {
                    "event": "delete_slide/execute",
                    "slide_id": slide_id
                }
            )
        slide_image = images[0]
        
        await self._slide_repo.delete_by_id(slide_id)

        await self.delete_image(
            slide_image.public_id,
            saga_service,
            action_func=action_func,
            compensation_func=compensation_func
        )

        await self._invalidate_slides()


    async def _get_last_order(self) -> int:
        return (await self._slide_repo.count_all(SlideFiltersCommand(activo=True)))+1
    
    async def _get_slides_data(
            self,
            command_filters: SlideFiltersCommand,
            offset:int,
            limit:int,
            total_pages: int,
            current_page: int
    ) -> dict:
        slides = await self._slide_repo.get_slides_with_filter(command_filters, offset, limit)

        images: list[ImageEntity] = await self._image_repo.get_by_owners(
            owner_type="slide",
            owner_ids=[slide.id for slide in slides if slide.id is not None]
        )

        images_key_value: dict[int, ImageEntity] = {image.owner_id: image for image in images if image.owner_id}

        for slide in slides:
            slide.sync_image(images_key_value)
        
        return {
            "slides": [
                slide.to_dict
                for slide in slides
            ],
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            }
        }

    async def _invalidate_slides(self) -> None:
        args = self._cache_strategy.operation_list("slides", {})
        family_key = self._cache_strategy.generate_family_key(args)
        await self._cache_service.invalidate_family(family_key)