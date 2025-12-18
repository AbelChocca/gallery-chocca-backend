from app.api.v1.slides.slide_route import router
from app.api.schemas.slides.slide_schema import ReadSlideSchema, SlideFilterSchema
from app.api.schemas.slides.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.api.dependencies.slides.case_depends import get_slides_case
from app.application.slides.cases.get_slides import GetSlidesCase

from fastapi import status, Depends, Query
from typing import List

@router.post(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[ReadSlideSchema],
    summary="Get all slides with filters"
)
async def get_slides(
    schema_filters: SlideFilterSchema,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    case: GetSlidesCase = Depends(get_slides_case)
) -> List[ReadSlideSchema]:
    slides_dto = await case.exec(
        offset=offset, 
        limit=limit, filters_command=InputSchemaMapper.to_filters_command(schema_filters)
        )
    return [
        OutputSchemaMapper.to_schema(slide)
        for slide in slides_dto
    ]