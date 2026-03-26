from app.domain.slide.slide_dto import SlideFiltersCommand
from app.application.slides.service import SlideService

class GetSlidesCase:
    def __init__(
            self,
            slide_service: SlideService,
            ):
        self._slide_service = slide_service

    async def exec(
            self, 
            *,
            page: int, 
            limit:int, 
            filters_command: SlideFiltersCommand
        ) -> dict:
        return await self._slide_service.get_slides(page, limit, filters_command)