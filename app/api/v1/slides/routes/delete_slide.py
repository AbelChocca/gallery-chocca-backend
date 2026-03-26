from app.api.v1.slides.slide_route import router
from app.api.dependencies.slides.case_depends import get_delete_slide_case
from app.application.slides.cases.delete_slide import DeleteSlideCase
from app.api.security.resolvers.sessions import get_admin_session

from fastapi import Depends, status, Path
from typing import Dict, Any, Annotated

@router.delete(
    "/{slide_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an Slide by her id"
)
async def delete_slide(
    slide_id: Annotated[int, Path(title="The slide's id for delete it.")], 
    case: Annotated[DeleteSlideCase, Depends(get_delete_slide_case)],
    _: Annotated[None, Depends(get_admin_session)]
    ) -> Dict[str, Any]:
    return await case.execute(slide_id)