from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.slide_entity import SlideEntity
from app.shared.dto.slide_dto import SlideFiltersDTO

from typing import List

class GetSlidesCase:
    def __init__(
            self,
            repo: SlideRepository
            ):
        self.repo = repo

    async def exec(self, offset:int, limit:int, filters_dto: SlideFiltersDTO) -> List[SlideEntity]:
        slides = await self.repo.get_slides_with_filter(filters_dto, offset, limit)

        return slides