from app.features.slides.slide_route import router
from app.api.security.resolvers.sessions import get_admin_session
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService

from fastapi import Depends, status, Path
from typing import Dict, Any, Annotated

@router.delete(
    "/{slide_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an Slide by her id"
)
async def delete_slide(
    slide_id: Annotated[int, Path(title="The slide's id for delete it.")], 
    service: Annotated[SlideService, Depends(get_slide_service)],
    _: Annotated[None, Depends(get_admin_session)]
    ) -> Dict[str, Any]:
    return await service.delete_slide(slide_id)