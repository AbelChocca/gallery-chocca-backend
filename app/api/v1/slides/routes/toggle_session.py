from app.api.v1.slides.slide_route import router
from app.application.slides.cases.toggle_session import ToggleSlideSessionCase
from app.api.dependencies.slides.case_depends import get_toggle_slide_session_case

from fastapi import status, Depends, Query, Path
from typing import Annotated

@router.patch(
    "/toggle_session/{slide_id}",
    status_code=status.HTTP_200_OK
)
async def toggle_session(
    slide_id: Annotated[int, Path(...)],
    is_active: Annotated[bool, Query(...)],
    case: Annotated[ToggleSlideSessionCase, Depends(get_toggle_slide_session_case)]
) -> None:
    await case.execute(slide_id, is_active)