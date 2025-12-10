from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.slide_entity import SlideEntity
from app.shared.dto.slide_dto import SlideDTO
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException
from app.shared.exceptions.domain.slide_exception import SlideNotFound


class PublishSlideCase:
    def __init__(
            self,
            repo: SlideRepository
            ):
        self.repo = repo

    async def exec(self, slide_dto: SlideDTO) -> SlideEntity:
        slide = SlideEntity(
            imagen_url=slide_dto.imagen_url,
            enlace_boton=slide_dto.enlace_boton,
            cloudinary_id=slide_dto.cloudinary_id,
            activo=slide_dto.activo,
            orden=slide_dto.orden,
            fecha_actualizada=slide_dto.fecha_actualizada,
            fecha_creada=slide_dto.fecha_creada
        )
        slide = await self.repo.save(slide)
        return slide
