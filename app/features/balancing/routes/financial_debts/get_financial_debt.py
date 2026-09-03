from fastapi import Depends, status

from app.features.balancing.schemas.financial_debt_schema import FinancialDebtResponseSchema
from app.features.balancing.services.financial_debt_service import FinancialDebtService
from app.features.balancing.routes.financial_debts.financial_debt_router import financial_debt_router
from app.features.balancing.dependencies.financial_debt.service import get_financial_debt_service



@financial_debt_router.get(
    "/{financial_debt_id}",
    response_model=FinancialDebtResponseSchema,
)
async def get_financial_debt(
    financial_debt_id: int,
    service: FinancialDebtService = Depends(
        get_financial_debt_service
    ),
):
    result = await service.get_by_id(financial_debt_id)

    return FinancialDebtResponseSchema.model_validate(result)