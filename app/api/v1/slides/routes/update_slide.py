from app.api.v1.slides.slide_route import router
from app.api.dependencies.slides.case_depends import get_update_slide_case
from app.api.schemas.slides.slide_schema import ReadSlideSchema, UpdateSlideSchema
from app.api.schemas.slides.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.application.slides.cases.update_slide import UpdateSlideCase
from app.api.security.dependencies.sessions import get_admin_session

from fastapi import status, Depends, UploadFile, File, Path, Form
from fastapi.concurrency import run_in_threadpool
from typing import Annotated, Optional
from json import loads


@router.patch(
    "/{slide_id}",
    response_model=ReadSlideSchema,
    status_code=status.HTTP_200_OK,
    summary="Update an slide by her id"
)
async def update_slide(
    slide_id: Annotated[int, Path(...)],
    update_slide_json: Annotated[str, Form(...)],
    case: Annotated[UpdateSlideCase, Depends(get_update_slide_case)],
    _: Annotated[None, Depends(get_admin_session)],
    new_image: Annotated[Optional[UploadFile], File()] = None
) -> ReadSlideSchema:
    data = loads(update_slide_json)
    new_slide_schema = UpdateSlideSchema(**data)
    slide_dto = await run_in_threadpool(
        case.execute,
        slide_id, 
        InputSchemaMapper.to_update_command(new_slide_schema),
        new_image.file or None
        )
    return OutputSchemaMapper.to_schema(slide_dto)