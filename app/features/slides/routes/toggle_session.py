from app.features.slides.slide_route import router
from app.api.security.resolvers.sessions import get_admin_session
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService

from fastapi import status, Depends, Query, Path
from typing import Annotated

@router.patch(
    "/toggle_session/{slide_id}",
    status_code=status.HTTP_200_OK
)
async def toggle_session(
    slide_id: Annotated[int, Path(...)],
    is_active: Annotated[bool, Query(...)],
    service: Annotated[SlideService, Depends(get_slide_service)],
    _: Annotated[None, Depends(get_admin_session)]
) -> None:
    await service.toggle_slide_session(slide_id, is_active)