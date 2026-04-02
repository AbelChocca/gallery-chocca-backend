
from app.application.slides.service import SlideService


class ToggleSlideSessionCase:
    def __init__(
        self,
        slide_service: SlideService
    ):
        self._slide_service = slide_service

    async def execute(
        self,
        slide_id: int,
        is_active: bool
    ) -> None:
        await self._slide_service.toggle_slide_session(slide_id, is_active)