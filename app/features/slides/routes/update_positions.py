from app.features.slides.slide_route import router
from app.features.slides.slide_schema import UpdateSlidesOrderSchema
from app.features.slides.schema_mapper import InputSchemaMapper
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Body
from typing import Annotated

@router.patch(
    '/positions',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Update the positions of existing slides',
    dependencies=[
        require_permission(Permission.SLIDE_UPDATE)
    ]
)
async def update_positions(
    input: Annotated[UpdateSlidesOrderSchema, Body(..., title="Schema of the update slide position")],
    service: Annotated[SlideService, Depends(get_slide_service)]
):
    command = InputSchemaMapper.to_update_order(input)
    await service.update_positions(command)