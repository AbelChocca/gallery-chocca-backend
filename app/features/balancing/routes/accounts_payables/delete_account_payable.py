from fastapi import Depends, status

from app.features.balancing.services.accounts_payable_service import AccountsPayableService

from app.features.balancing.routes.accounts_payables.account_payable_router import accounts_payable_router
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service


@accounts_payable_router.delete(
    "/{accounts_payable_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_accounts_payable(
    accounts_payable_id: int,
    service: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
) -> None:
    await service.delete(accounts_payable_id)