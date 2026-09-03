from fastapi import Depends

from app.features.balancing.services.accounts_payable_service import AccountsPayableService
from app.features.balancing.schemas.accounts_payable_schema import AccountsPayableFilterSchema, AccountsPayableResponseSchema

from app.features.balancing.routes.accounts_payables.account_payable_router import accounts_payable_router
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service


@accounts_payable_router.get(
    "",
    response_model=list[AccountsPayableResponseSchema],
)
async def get_accounts_payables(
    filters: AccountsPayableFilterSchema = Depends(),
    service: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
):
    result = await service.find(
        balance_snapshot_id=filters.balance_snapshot_id,
        brand=filters.brand,
        cost_center=filters.cost_center,
        status=filters.status,
    )

    return result