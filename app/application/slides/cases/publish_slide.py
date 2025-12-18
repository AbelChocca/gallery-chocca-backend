from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.dto import ReadSlideDTO
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.modules.slide.domain.slide_entity import SlideEntity
from app.application.slides.commands import PublishSlideCommand

from typing import IO


class PublishSlideCase:
    def __init__(
            self,
            repo: SlideRepository,
            image_repo: CloudinaryRepository
            ):
        self.repo = repo
        self.image_repo = image_repo

    async def exec(self, image_file: IO[bytes], command: PublishSlideCommand) -> ReadSlideDTO:
        cloud_image = self.image_repo.upload_image(image_file, "slides")
        slide = SlideEntity(
            imagen_url=cloud_image.url,
            enlace_boton=command.enlace_boton,
            cloudinary_id=cloud_image.public_id,
            activo=command.activo,
            orden=command.orden,
        )
        slide = await self.repo.save(slide)
        return ReadSlideDTO(
            imagen_url=slide.imagen_url,
            activo=slide.activo,
            orden=slide.orden,
            cloudinary_id=slide.cloudinary_id,
            id=slide.id,
            enlace_boton=slide.enlace_boton,
            fecha_creada=slide.fecha_creada,
            fecha_actualizada=slide.fecha_actualizada
        )
