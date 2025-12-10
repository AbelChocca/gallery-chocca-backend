from app.modules.product.interface.product_route import router
from app.modules.product.interface.schema.schema import ProductRead, UpdateProductSchema
from app.modules.product.interface.schema.schema_mapper import ProductSchemaMapper
from app.modules.product.domain.use_cases.update_product import UpdateProductCase
from app.modules.product.interface.dependencies.case_depends import get_update_product_case
from app.core.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import status, Depends

@router.patch(
    "/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
    summary="Update an product"
)
async def update_product(
    update_schema: UpdateProductSchema,
    product_id: int,
    case: UpdateProductCase = Depends(get_update_product_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> UpdateProductSchema:
    await auth_session.get_admin()
    dto = ProductSchemaMapper.to_update_dto(update_schema)
    res = await case.execute(dto, product_id)
    return ProductSchemaMapper.entity_to_schema(res)