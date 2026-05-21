from app.features.slides.slide_route import router
from app.features.slides.slide_schema import UpdateSlidesOrderSchema
from app.features.slides.schema_mapper import InputSchemaMapper
from app.api.security.resolvers.sessions import get_admin_session
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService

from fastapi import status, Depends, Body
from typing import Annotated

@router.patch(
    '/positions',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Update the positions of existing slides'
)
async def update_positions(
    input: Annotated[UpdateSlidesOrderSchema, Body(..., title="Schema of the update slide position")],
    service: Annotated[SlideService, Depends(get_slide_service)],
    _: Annotated[None, Depends(get_admin_session)]
):
    command = InputSchemaMapper.to_update_order(input)
    await service.update_positions(command)