from fastapi import Depends, status

from app.features.balancing.types.accounts_payable_types import AccountsPayableUpdate
from app.features.balancing.services.accounts_payable_service import AccountsPayableService
from app.features.balancing.schemas.accounts_payable_schema import AccountsPayableUpdateSchema

from app.features.balancing.routes.accounts_payables.account_payable_router import accounts_payable_router
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service

@accounts_payable_router.put(
    "/{accounts_payable_id}",
    status_code=status.HTTP_200_OK,
)
async def update_accounts_payable(
    accounts_payable_id: int,
    payload: AccountsPayableUpdateSchema,
    service: AccountsPayableService = Depends(get_accounts_payable_service),
):
    update_dto = AccountsPayableUpdate(
        brand=payload.brand,
        entity_name=payload.entity_name,
        cost_center=payload.cost_center,
        amount=payload.amount,
        status=payload.status,
        fields_set=payload.model_fields_set
    )

    return await service.update(
        accounts_payable_id,
        update_dto,
    )