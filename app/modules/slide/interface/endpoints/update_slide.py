from app.modules.slide.interface.slide_route import router
from app.modules.slide.interface.dependencies.case_depends import get_update_slide_case
from app.modules.slide.interface.schema.slide_schema import ReadSlideSchema, UpdateSlideSchema
from app.modules.slide.interface.schema.schema_mapper import SlideSchemaMapper
from app.modules.slide.domain.cases.update_slide import UpdateSlideCase
from app.core.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import status, Depends

@router.patch(
    "/{slide_id}",
    response_model=ReadSlideSchema,
    status_code=status.HTTP_200_OK,
    summary="Update an slide by her id"
)
async def update_slide(
    slide_id: int,
    new_slide_schema: UpdateSlideSchema,
    case: UpdateSlideCase = Depends(get_update_slide_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> ReadSlideSchema:
    await auth_session.get_admin()
    slide = await case.execute(slide_id, new_slide_schema)
    return SlideSchemaMapper.entity_to_schema(slide)