from app.modules.product.interface.product_route import router
from app.modules.product.interface.schema.schema import ProductRead, CreateProductSchema
from app.modules.product.interface.dependencies.case_depends import get_create_product_case
from app.modules.product.interface.schema.schema_mapper import ProductSchemaMapper
from app.core.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from app.modules.product.domain.use_cases.create_product import CreateProductUseCase

from fastapi import status, Depends

@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an product"
)
async def create_product(
    schema: CreateProductSchema,
    case: CreateProductUseCase = Depends(get_create_product_case),
    admin_auth: SecuritySessions = Depends(get_auth_sessions)
) -> ProductRead:
    await admin_auth.get_admin()
    res = await case.execute(ProductSchemaMapper.to_create_dto(schema))
    return ProductSchemaMapper.entity_to_schema(res)
