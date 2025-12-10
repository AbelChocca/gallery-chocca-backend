from app.modules.slide.interface.slide_route import router
from app.modules.slide.interface.schema.slide_schema import ReadSlideSchema, SlideFilterSchema
from app.modules.slide.interface.schema.schema_mapper import SlideSchemaMapper
from app.modules.slide.interface.dependencies.case_depends import get_slides_case
from app.modules.slide.domain.cases.get_slides import GetSlidesCase

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
    slides = await case.exec(offset=offset, limit=limit, filters_dto=SlideSchemaMapper.to_filters_dto(schema_filters))
    return [
        SlideSchemaMapper.entity_to_schema(slide)
        for slide in slides
    ]