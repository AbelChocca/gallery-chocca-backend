from fastapi import Depends, status

from app.features.balancing.services.accounts_payable_service import AccountsPayableService
from app.features.balancing.schemas.accounts_payable_schema import AccountsPayableCreateSchema, AccountsPayableResponseSchema
from app.features.balancing.entities.accounts_payable import AccountsPayable

from app.features.balancing.routes.accounts_payables.account_payable_router import accounts_payable_router
from app.features.balancing.dependencies.accounts_payable.service import get_accounts_payable_service

@accounts_payable_router.post(
    "",
    response_model=AccountsPayableResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_accounts_payable(
    schema: AccountsPayableCreateSchema,
    service: AccountsPayableService = Depends(
        get_accounts_payable_service
    ),
) -> AccountsPayableResponseSchema:

    entity = AccountsPayable(
        balance_snapshot_id=schema.balance_snapshot_id,
        brand=schema.brand,
        entity_name=schema.entity_name,
        cost_center=schema.cost_center,
        amount=schema.amount,
        status=schema.status,
    )

    result = await service.create(entity)

    return AccountsPayableResponseSchema.model_validate(result)