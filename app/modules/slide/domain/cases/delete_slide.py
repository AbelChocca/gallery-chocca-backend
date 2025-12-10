from app.modules.slide.domain.slide_repository import SlideRepository
from app.shared.exceptions.domain.slide_exception import SlideNotFound
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException

from typing import Dict, Any

class DeleteSlideCase:
    def __init__(
            self,
            repo: SlideRepository
            ):
        self.repo = repo


    async def execute(self, slide_id: int) -> Dict[str, Any]:
        await self.repo.delete_by_id(slide_id=slide_id)
        return {"message": f"Slide with id: {slide_id} was deleted."}
            