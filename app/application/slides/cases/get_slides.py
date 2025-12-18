from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.dto import ReadSlideDTO
from app.application.slides.commands import SlideFiltersCommand
from app.application.slides.helper_mapper import CommandToDTOInterpreter

from typing import List

class GetSlidesCase:
    def __init__(
            self,
            repo: SlideRepository
            ):
        self.repo = repo

    async def exec(self, offset:int, limit:int, filters_command: SlideFiltersCommand) -> List[ReadSlideDTO]:
        filters_dto = CommandToDTOInterpreter.to_filter_dto(filters_command)
        
        slides = await self.repo.get_slides_with_filter(filters_dto, offset, limit)

        return [
            ReadSlideDTO(
                imagen_url=slide.imagen_url,
                activo=slide.activo,
                orden=slide.orden,
                cloudinary_id=slide.cloudinary_id,
                id=slide.id,
                enlace_boton=slide.enlace_boton,
                fecha_actualizada=slide.fecha_actualizada,
                fecha_creada=slide.fecha_creada
            )
            for slide in slides
        ]