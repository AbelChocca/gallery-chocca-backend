from app.api.v1.slides.slide_route import router
from app.api.dependencies.slides.case_depends import get_update_slide_case
from app.api.schemas.slides.slide_schema import ReadSlideSchema, UpdateSlideSchema
from app.api.schemas.slides.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions
from app.application.slides.cases.update_slide import UpdateSlideCase

from fastapi import status, Depends, UploadFile, File

@router.patch(
    "/{slide_id}",
    response_model=ReadSlideSchema,
    status_code=status.HTTP_200_OK,
    summary="Update an slide by her id"
)
async def update_slide(
    slide_id: int,
    new_slide_schema: UpdateSlideSchema,
    new_image: UploadFile = File(None),
    case: UpdateSlideCase = Depends(get_update_slide_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> ReadSlideSchema:
    await auth_session.get_admin()
    slide_dto = await case.execute(
        slide_id=slide_id, 
        new_slide_command=InputSchemaMapper.to_update_command(new_slide_schema),
        new_image=new_image.file
        )
    return OutputSchemaMapper.to_schema(slide_dto)