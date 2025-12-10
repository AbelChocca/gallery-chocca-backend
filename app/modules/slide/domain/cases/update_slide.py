from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.slide_entity import SlideEntity

from app.shared.dto.slide_dto import UpdateSlideDTO
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException
from app.shared.exceptions.domain.slide_exception import SlideNotFound

class UpdateSlideCase:
    def __init__(
            self,
            repo: SlideRepository
            ):
        self.repo = repo

    async def execute(self, slide_id: int, new_slide_dto: UpdateSlideDTO) -> SlideEntity:
        slide = await self.repo.get_by_id(slide_id)

        slide.update_slide(new_slide_dto)

        return await self.repo.save(slide)