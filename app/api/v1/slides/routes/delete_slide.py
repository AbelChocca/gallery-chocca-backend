from app.api.v1.slides.slide_route import router
from app.api.dependencies.slides.case_depends import get_delete_slide_case
from app.application.slides.cases.delete_slide import DeleteSlideCase
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import Depends, status
from typing import Dict, Any

@router.delete(
    "/{slide_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an Slide by her id"
)
async def delete_slide(
    slide_id: int, 
    case: DeleteSlideCase = Depends(get_delete_slide_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
    ) -> Dict[str, Any]:
    await auth_session.get_admin()
    return await case.execute(slide_id)