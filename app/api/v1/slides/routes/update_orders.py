from app.api.v1.slides.slide_route import router
from app.api.dependencies.slides.case_depends import get_update_slide_orders_case
from app.application.slides.cases.update_orders import UpdateOrdersCase
from app.api.schemas.slides.slide_schema import UpdateSlidesOrderSchema
from app.api.schemas.slides.schema_mapper import InputSchemaMapper

from fastapi import status, Depends, Body
from typing import Annotated

@router.patch(
    '/update_orders',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Update the orders of existing slides'
)
async def update_orders(
    input: Annotated[UpdateSlidesOrderSchema, Body(..., title="Schema of the update slide order")],
    case: Annotated[UpdateOrdersCase, Depends(get_update_slide_orders_case)]
):
    command = InputSchemaMapper.to_update_order(input)
    await case.execute(command)