from app.features.slides.slide_route import router
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import Depends, status, Path
from typing import Dict, Any, Annotated

@router.delete(
    "/{slide_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an Slide by her id",
    dependencies=[
        require_permission(Permission.SLIDE_DELETE)
    ]
)
async def delete_slide(
    slide_id: Annotated[int, Path(title="The slide's id for delete it.")], 
    service: Annotated[SlideService, Depends(get_slide_service)],
    ) -> Dict[str, Any]:
    return await service.delete_slide(slide_id)