from app.features.slides.slide_route import router
from app.features.slides.slide_schema import UpdateSlideSchema
from app.features.slides.schema_mapper import InputSchemaMapper
from app.features.slides.types import SlideImageType
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, File, Path, Form
from typing import Annotated
import orjson

@router.patch(
    "/{slide_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update an slide by her id",
    dependencies=[
        require_permission(Permission.SLIDE_UPDATE)
    ]
)
async def update_slide( 
    slide_id: Annotated[int, Path(...)],
    update_slide_json: Annotated[str, Form(...)],
    service: Annotated[SlideService, Depends(get_slide_service)],
    new_image: SlideImageType = File(None),
) -> None:
    data = orjson.loads(update_slide_json)
    new_slide_schema = UpdateSlideSchema(**data)
    await service.update_slide(
        slide_id, 
        InputSchemaMapper.to_update_command(new_slide_schema),
        new_image.file if new_image is not None else None
        )