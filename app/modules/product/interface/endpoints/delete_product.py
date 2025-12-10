from app.modules.product.interface.product_route import router
from app.modules.product.domain.use_cases.delete_product import DeleteProductCase
from app.modules.product.interface.dependencies.case_depends import get_delete_product_case
from app.core.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import status, Depends
from typing import Dict

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an product by her id"
)
async def delete_product(
    product_id: int,
    case: DeleteProductCase = Depends(get_delete_product_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> Dict[str, str]:
    await auth_session.get_admin()
    await case.execute(product_id)
    return {"message": "Product was deleted successfully"}