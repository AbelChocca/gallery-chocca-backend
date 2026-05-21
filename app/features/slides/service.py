from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.repositories.sqlmodel_slide_repository import PostgresSlideRepository
from app.shared.pagination.pagination_service import PaginationService
from app.infra.saga_service import SagaService
from app.infra.cache.protocole import CacheProtocol
from app.features.slides.dto import UpdateSlideCommand, UpdateSlidesOrder, SlideFiltersCommand, PublishSlideCommand
from app.features.media.entities.image import ImageEntity
from app.features.slides.types import SlidesOverview, ActiveAndInactiveSlides
from app.features.media.service import MediaService

from app.features.slides.entity import SlideEntity
from app.core.exceptions import ValueNotFound, ValidationError
from app.core.app_exception import AppException
import random

from typing import Any, BinaryIO

class SlideService:
    def __init__(
            self,
            slide_repo: PostgresSlideRepository,
            image_repo: PostgresImageRepository,
            media_service: MediaService,
            saga_service: SagaService,
            pagination_service: PaginationService,
            cache_service: CacheProtocol,
        ):
        self._cache_service = cache_service
        self._pagination_service = pagination_service
        self._media_service = media_service
        self._saga_service = saga_service
        self._slide_repo = slide_repo
        self._image_repo = image_repo

    async def toggle_slide_session(self, slide_id: int, is_active: bool) -> None:
        await self._slide_repo.toggle_slide_session(slide_id, is_active)

        await self._cache_service.invalidate_entities("slides")
    
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
        
    async def update_slide(
        self,
        slide_id: int,
        command: UpdateSlideCommand,
        new_image_file: BinaryIO | None = None
    ) -> None:
        slide = await self.get_by_id(slide_id)

        if not command.delete_image and new_image_file is not None and slide.has_image:
            raise ValidationError(
                "Current slide's image need to be deleted before upload a new image for the same slide.",
                {
                    "module": "slides",
                    "case": "update_slide_case",
                    "event": "case/execute",
                }
            )
        
        if command.delete_image and slide.has_image:
            slide.image = await self._media_service.delete_image(
                image_public_id=slide.image_public_id,
                saga_service=self._saga_service
            )

        if slide.is_inactive and command.activo:
            slide.orden = await self._get_last_order()
        elif slide.activo and not command.activo:
            slide.orden = random.randint(999, 9999)

        slide.update_slide(command.to_dict)

        if not slide.has_image and new_image_file is not None:
            await self._media_service.create_image(
                image_resource=new_image_file,
                folder="slides",
                owner_id=slide.id,
                owner_type="slide",
                saga_service=self._saga_service
            )

        await self._slide_repo.save(slide)

        await self._cache_service.invalidate_entities("slides")

    async def update_positions(
            self,
            command: UpdateSlidesOrder
    ) -> None:
        if not command.slides:
            return None 
        
        self._validate_positions(command.positions, command.ids)

        updates = [slide.to_dict for slide in command.slides]

        await self._slide_repo.update_many_orders(command.ids, updates)

        await self._cache_service.invalidate_entities("slides")

    async def get_slides(
        self,
        page: int, 
        limit:int, 
        filters_command: SlideFiltersCommand
    ) -> dict[str, Any]:
        offset: int = self._pagination_service.get_offset(page, limit)

        total_slides: int = await self._slide_repo._count_all(filters_command)

        total_pages: int = self._pagination_service.get_total_pages(total_slides, limit)
        current_page: int = self._pagination_service.get_current_page(offset, limit)

        return await self._cache_service.get_or_set_with_lock(
            "slides",
            callback=self._get_slides_data,
            kwargs={
                "command_filters": filters_command,
                "offset": offset,
                "limit": limit,
                "total_pages": total_pages,
                "current_page": current_page
            },
            key_args={
                "filters": filters_command.to_dict, 
                "page": page, 
                "limit": limit
            }
        )
    
    async def create_slide(
        self,
        command: PublishSlideCommand,
        image_file: BinaryIO,
    ) -> None:
        try:
            slide = SlideEntity(
                enlace_boton=command.enlace_boton,
                activo=command.activo,
            )
            if slide.activo:
                slide.orden = await self._get_last_order()

            slide = await self._slide_repo.save(slide)

            await self._media_service.create_image(
                image_resource=image_file,
                folder="slides",
                owner_id=slide.id,
                owner_type="slide",
                saga_service=self._saga_service
            )

            await self._cache_service.invalidate_entities("slides")
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae

    async def delete_slide(
            self,
            slide_id: int
    ) -> dict:
        try:
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

            await self._media_service.delete_image(image_public_id=slide_image.id, saga_service=self._saga_service)

            await self._cache_service.invalidate_entities("slides")

            return {"message": f"Slide with id: {slide_id} was deleted."}
        except AppException as ae:
            await self._saga_service.compensate_all()
            
            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae

    async def overview(self) -> SlidesOverview:
        num_slides = await self._count_slides
        active_and_inactive_slides = await self._count_slides_by_active_session()
        last_three_slides = await self._get_last_n_slides(3)

        res: SlidesOverview = {
            "last_three_slides": last_three_slides,
            "total_slides": num_slides,
            "sessions_count": active_and_inactive_slides
        }
        return res

    async def _get_last_order(self) -> int:
        return await self._slide_repo._get_last_order()
    
    async def _get_slides_data(
            self,
            command_filters: SlideFiltersCommand,
            offset:int,
            limit:int,
            total_pages: int,
            current_page: int
    ) -> dict:
        slides = await self._enrich_slides(
            await self._slide_repo.get_slides_with_filter(command_filters, offset, limit)
        )
        
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
    
    async def _get_last_n_slides(self, n: int) -> list[dict]:
        slides = await self._enrich_slides(
            await self._slide_repo.get_last_n_slides(n)
        )
        return [
            slide.to_dict
            for slide in slides
        ] 
    
    async def _count_slides_by_active_session(self) -> ActiveAndInactiveSlides:
        slides_by_active_session = await self._slide_repo.count_slides_by_active_session()

        res: ActiveAndInactiveSlides = {
            "active" if session else "inactive": count
            for session, count in slides_by_active_session
        }
    
    
    async def _enrich_slides(
            self,
            slides: list[SlideEntity]
    ) -> list[SlideEntity]:
        images: list[ImageEntity] = await self._image_repo.get_by_owners(
            owner_type="slide",
            owner_ids=[slide.id for slide in slides if slide.id is not None]
        )

        images_key_value: dict[int, ImageEntity] = {image.owner_id: image for image in images if image.owner_id}

        for slide in slides:
            slide.sync_image(images_key_value)
        
        return slides
    
    async def _count_slides(self) -> int:
        return await self._slide_repo.count_all()
    
    def _validate_positions(self, new_positions: list[int], ids: list[int]) -> None:
        if not new_positions:
            raise ValidationError(
                "'new_positions' musn't be empty",
                {
                    "module": "slides",
                    "case": "update_orders_case",
                    "event": "_validate_orders"
                }
            )

        if len(new_positions) != len(set(new_positions)):
            raise ValidationError(
                "The order of slides cannot be repeated",
                {
                    "module": "slides",
                    "case": "update_orders_case",
                    "event": "_validate_orders"
                }
            )
        
        if len(ids) != len(set(ids)):
            raise ValidationError(
                "Slide ids cannot be repeated",
                {
                    "module": "slides",
                    "case": "update_orders_case",
                    "event": "_validate_orders"
                }
            )