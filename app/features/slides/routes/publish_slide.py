from app.features.slides.slide_route import router
from app.features.slides.slide_schema import PublishSlideSchema
from app.features.slides.schema_mapper import InputSchemaMapper
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import Depends, status, UploadFile, File, Form
from json import loads
from typing import Annotated

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Publish an slide",
    dependencies=[
        require_permission(Permission.SLIDE_CREATE)
    ]
)
async def publish_slide(
    publish_slide_json: Annotated[str, Form(...)],
    image_file: Annotated[UploadFile, File(...)],
    service: Annotated[SlideService, Depends(get_slide_service)],
) -> None:
    data = loads(publish_slide_json)
    slide_schema: PublishSlideSchema = PublishSlideSchema(**data)
    await service.create_slide(
        image_file=image_file.file, 
        command=InputSchemaMapper.publish_command(slide_schema)
        )