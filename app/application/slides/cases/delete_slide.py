from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.slide_entity import SlideEntity
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository

from typing import Dict, Any

class DeleteSlideCase:
    def __init__(
            self,
            repo: SlideRepository,
            image_repo: CloudinaryRepository
            ):
        self.repo = repo
        self.image_repo = image_repo


    async def execute(self, slide_id: int) -> Dict[str, Any]:
        """
        Delete slide from database and his image from cloud service, by his id
        
        :param self: Default
        :param slide_id: Slide ID
        :type slide_id: int
        :return: Dictionary with a message of successful
        :rtype: Dict[str, Any]
        """
        slide_to_delete: SlideEntity = self.repo.get_by_id(slide_id) 

        self.image_repo.delete_image(slide_to_delete.imagen_url)

        await self.repo.delete_by_id(slide_id=slide_id)
        return {"message": f"Slide with id: {slide_id} was deleted."}
            