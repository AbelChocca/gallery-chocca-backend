from app.modules.slide.interface.slide_route import router
from app.modules.slide.interface.schema.slide_schema import ReadSlideSchema, PublishSlideSchema
from app.modules.slide.interface.dependencies.case_depends import get_publish_slide_case
from app.modules.slide.interface.schema.schema_mapper import SlideSchemaMapper
from app.modules.slide.domain.cases.publish_slide import PublishSlideCase
from app.core.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import Depends, status

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadSlideSchema,
    summary="Publish an slide"
)
async def publish_slide(
    slide_schema: PublishSlideSchema,
    case: PublishSlideCase = Depends(get_publish_slide_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> ReadSlideSchema:
    await auth_session.get_admin()
    return await case.exec(SlideSchemaMapper.publish_dto(slide_schema))