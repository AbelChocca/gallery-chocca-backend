from app.api.v1.products.product_route import router
from app.application.products.cases.delete_product import DeleteProductCase
from app.api.dependencies.products.case_depends import get_delete_product_case
from app.api.security.dependencies.sessions import get_admin_session

from fastapi import status, Depends, Path
from fastapi.concurrency import run_in_threadpool
from typing import Dict, Annotated

@router.delete(
    "/delete/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an product by her id"
)
async def delete_product(
    product_id: Annotated[int, Path(title="ID of the product to delete")],
    case: Annotated[DeleteProductCase, Depends(get_delete_product_case)],
    _: Annotated[None, Depends(get_admin_session)]
) -> Dict[str, str]:
    await run_in_threadpool(case.execute, product_id)
    return {"message": "Product was deleted successfully"}