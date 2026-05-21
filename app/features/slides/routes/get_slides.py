from app.features.slides.slide_route import router
from app.features.slides.slide_schema import SlideFilterSchema, GetSlidesResponseSchema
from app.features.slides.schema_mapper import InputSchemaMapper
from app.shared.pagination.schema import PaginationSchema
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService

from fastapi import status, Depends
from typing import Annotated

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=GetSlidesResponseSchema,
    summary="Get all slides with filters"
)
async def get_slides(
    schema_filters: Annotated[SlideFilterSchema, Depends()],
    pagination: Annotated[PaginationSchema, Depends()],
    service: Annotated[SlideService, Depends(get_slide_service)]
) -> GetSlidesResponseSchema:
    slides_data = await service.get_slides(
        page=pagination.page, 
        limit=pagination.limit, 
        filters_command=InputSchemaMapper.to_filters_command(schema_filters)
        )
    return GetSlidesResponseSchema(**slides_data)