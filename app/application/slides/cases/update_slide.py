from app.core.log.logger_repository import LoggerRepository
from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.domain.dto import ReadSlideDTO
from app.application.slides.commands import UpdateSlideCommand
from app.application.slides.helper_mapper import CommandToDTOInterpreter

from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository

from typing import Optional, BinaryIO

class UpdateSlideCase:
    def __init__(
            self,
            repo: SlideRepository,
            image_repo: CloudinaryRepository,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.image_repo = image_repo
        self.logger = logger

    async def execute(
        self, 
        slide_id: int, 
        new_slide_command: UpdateSlideCommand,
        new_image: Optional[BinaryIO] = None
    ) -> ReadSlideDTO:
        slide = await self.repo.get_by_id(slide_id)

        if new_slide_command.delete_image and slide.cloudinary_id:
            self.image_repo.delete_image(slide.cloudinary_id)

            slide.actualizar_image(
                new_public_id="",
                new_url=""
            )
            if not new_image:
                slide.desactivar_slide()
                self.logger.warning(f"Se desactivo el slide con el id={slide.id} por no contar con imagen")

        slide.update_slide(CommandToDTOInterpreter.to_update_dto(new_slide_command))

        if new_image is not None:
            cloud_image = self.image_repo.upload_image(new_image, "slides")

            slide.actualizar_image(
                new_public_id=cloud_image.public_id,
                new_url=cloud_image.url
            )
            slide.slide_on()

        new_slide = await self.repo.save(slide)

        return ReadSlideDTO(
            imagen_url=new_slide.imagen_url,
            activo=new_slide.activo,
            orden=new_slide.orden,
            cloudinary_id=new_slide.cloudinary_id,
            id=new_slide.id,
            enlace_boton=new_slide.enlace_boton,
            fecha_creada=new_slide.fecha_creada,
            fecha_actualizada=new_slide.fecha_actualizada
        )
