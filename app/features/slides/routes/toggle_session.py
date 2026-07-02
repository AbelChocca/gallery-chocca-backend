from app.features.slides.slide_route import router
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Query, Path
from typing import Annotated

@router.patch(
    "/toggle_session/{slide_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_permission(Permission.SLIDE_UPDATE)
    ]
)
async def toggle_session(
    slide_id: Annotated[int, Path(...)],
    is_active: Annotated[bool, Query(...)],
    service: Annotated[SlideService, Depends(get_slide_service)]
) -> None:
    await service.toggle_slide_session(slide_id, is_active)