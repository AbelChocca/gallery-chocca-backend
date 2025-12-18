from app.api.v1.slides.slide_route import router
from app.api.schemas.slides.slide_schema import ReadSlideSchema, PublishSlideSchema
from app.api.dependencies.slides.case_depends import get_publish_slide_case
from app.api.schemas.slides.schema_mapper import InputSchemaMapper
from app.application.slides.cases.publish_slide import PublishSlideCase
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import Depends, status, UploadFile, File, Form
from json import loads
from typing import Annotated

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadSlideSchema,
    summary="Publish an slide"
)
async def publish_slide(
    publish_slide_json: Annotated[str, Form(...)],
    image_file: Annotated[UploadFile, File(...)],
    case: Annotated[PublishSlideCase, Depends(get_publish_slide_case)],
    auth_session: Annotated[SecuritySessions, Depends(get_auth_sessions)]
) -> ReadSlideSchema:
    await auth_session.get_admin()
    data = loads(publish_slide_json)
    slide_schema: PublishSlideSchema = PublishSlideSchema(**data)
    return await case.exec(image_file.file, InputSchemaMapper.publish_command(slide_schema))