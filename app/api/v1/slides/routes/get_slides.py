from app.api.v1.slides.slide_route import router
from app.api.schemas.slides.slide_schema import SlideFilterSchema, GetSlidesResponseSchema
from app.api.schemas.slides.schema_mapper import InputSchemaMapper
from app.api.schemas.pagination import PaginationSchema
from app.api.dependencies.slides.case_depends import get_slides_case
from app.application.slides.cases.get_slides import GetSlidesCase

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
    case: Annotated[GetSlidesCase, Depends(get_slides_case)]
) -> GetSlidesResponseSchema:
    slides_data = await case.exec(
        page=pagination.page, 
        limit=pagination.limit, 
        filters_command=InputSchemaMapper.to_filters_command(schema_filters)
        )
    return GetSlidesResponseSchema(**slides_data)