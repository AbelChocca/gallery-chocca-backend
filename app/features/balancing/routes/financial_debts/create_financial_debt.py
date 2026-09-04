from fastapi import Depends, status

from app.features.balancing.schemas.financial_debt_schema import FinancialDebtCreateSchema, FinancialDebtResponseSchema
from app.features.balancing.services.financial_debt_service import FinancialDebtService
from app.features.balancing.entities.financial_debt import FinancialDebt
from app.features.balancing.routes.financial_debts.financial_debt_router import financial_debt_router
from app.features.balancing.dependencies.financial_debt.service import get_financial_debt_service
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

@financial_debt_router.post(
    "",
    response_model=FinancialDebtResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[require_permission(Permission.BALANCE_CREATE)]
)
async def create_financial_debt(
    schema: FinancialDebtCreateSchema,
    service: FinancialDebtService = Depends(
        get_financial_debt_service
    ),
) -> FinancialDebtResponseSchema:

    entity = FinancialDebt(
        balance_snapshot_id=schema.balance_snapshot_id,
        bank_name=schema.bank_name,
        amount=schema.amount,
        status=schema.status,
    )

    result = await service.create(entity)

    return FinancialDebtResponseSchema.model_validate(result)