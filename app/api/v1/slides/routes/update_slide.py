from app.api.v1.slides.slide_route import router
from app.api.dependencies.slides.case_depends import get_update_slide_case
from app.api.schemas.slides.slide_schema import UpdateSlideSchema
from app.api.schemas.slides.schema_mapper import InputSchemaMapper
from app.application.slides.cases.update_slide import UpdateSlideCase
from app.api.security.resolvers.sessions import get_admin_session
from app.api.schemas.slides.types import SlideImageType

from fastapi import status, Depends, File, Path, Form
from typing import Annotated
import orjson

@router.patch(
    "/{slide_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update an slide by her id"
)
async def update_slide( 
    slide_id: Annotated[int, Path(...)],
    update_slide_json: Annotated[str, Form(...)],
    case: Annotated[UpdateSlideCase, Depends(get_update_slide_case)],
    _: Annotated[None, Depends(get_admin_session)],
    new_image: SlideImageType = File(None)
) -> None:
    data = orjson.loads(update_slide_json)
    new_slide_schema = UpdateSlideSchema(**data)
    await case.execute(
        slide_id, 
        InputSchemaMapper.to_update_command(new_slide_schema),
        new_image.file if new_image is not None else None
        )