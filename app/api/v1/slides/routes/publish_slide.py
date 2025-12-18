from app.api.v1.slides.slide_route import router
from app.api.schemas.slides.slide_schema import ReadSlideSchema, PublishSlideSchema
from app.api.dependencies.slides.case_depends import get_publish_slide_case
from app.api.schemas.slides.schema_mapper import InputSchemaMapper
from app.application.slides.cases.publish_slide import PublishSlideCase
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import Depends, status, UploadFile, File

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadSlideSchema,
    summary="Publish an slide"
)
async def publish_slide(
    slide_schema: PublishSlideSchema,
    image_file: UploadFile = File(...),
    case: PublishSlideCase = Depends(get_publish_slide_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> ReadSlideSchema:
    await auth_session.get_admin()
    return await case.exec(image_file.file, InputSchemaMapper.publish_command(slide_schema))