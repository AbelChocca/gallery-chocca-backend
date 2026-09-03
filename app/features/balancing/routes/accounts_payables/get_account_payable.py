from fastapi import Depends

from app.features.balancing.services.accounts_payable_service import AccountsPayableService
from app.features.balancing.schemas.accounts_payable_schema import AccountsPayableResponseSchema

from app.features.balancing.routes.accounts_payables.account_payable_router import accounts_payable_router
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service

@accounts_payable_router.get(
    "/{accounts_payable_id}",
    response_model=AccountsPayableResponseSchema,
)
async def get_accounts_payable(
    accounts_payable_id: int,
    service: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
):
    result = await service.get_by_id(accounts_payable_id)

    return AccountsPayableResponseSchema.model_validate(result)