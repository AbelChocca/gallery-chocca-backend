from app.modules.product.interface.dependencies.case_depends import get_product_by_id_case
from app.modules.product.interface.schema.schema import ProductRead
from app.modules.product.interface.schema.schema_mapper import ProductSchemaMapper
from app.modules.product.interface.product_route import router
from app.modules.product.domain.use_cases.get_product_by_id import GetProductByIDCase
from fastapi import status, Depends


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductRead,
    summary="Get an Product by her id"
)
async def get_product_by_id(
    product_id: int,
    case: GetProductByIDCase = Depends(get_product_by_id_case)
) -> ProductRead:
    product = await case.execute(product_id)
    return ProductSchemaMapper.entity_to_schema(product)