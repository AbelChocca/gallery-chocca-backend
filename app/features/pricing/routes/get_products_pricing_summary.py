from fastapi import Depends, status
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

from app.features.pricing.schema import (
    ProductsPricingSummaryResponse,
)
from app.shared.pagination.schema import PaginationSchema
from app.features.products.schema import FilterSchema
from app.features.products.parsers import filter_dep
from app.features.products.mappers.schema_mapper import InputSchemaMapper


@router.get(
    "/products/summary",
    status_code=status.HTTP_200_OK,
    response_model=ProductsPricingSummaryResponse
)
async def get_products_pricing_summary(
    filter_schema: Annotated[FilterSchema, Depends(filter_dep)],
    pagination: Annotated[PaginationSchema, Depends()],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):  
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)
    result =  await service.get_products_pricing_summary(
        filter_command=filter_command,
        limit=pagination.limit,
        page=pagination.page
    )

    return ProductsPricingSummaryResponse(**result)