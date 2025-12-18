from app.application.slides.commands import UpdateSlideCommand, SlideFiltersCommand
from app.modules.slide.domain.dto import UpdateSlideDTO, SlideFilterDTO

class CommandToDTOInterpreter:
    @staticmethod
    def to_update_dto(command: UpdateSlideCommand) -> UpdateSlideDTO:
        return UpdateSlideDTO(
            enlace_boton=command.enlace_boton,
            activo=command.activo,
            orden=command.orden
        )
    
    @staticmethod
    def to_filter_dto(command: SlideFiltersCommand) -> SlideFilterDTO:
        return SlideFilterDTO(
            activo=command.activo,
            fecha_actualizada=command.fecha_actualizada,
            fecha_creada=command.fecha_creada
        )