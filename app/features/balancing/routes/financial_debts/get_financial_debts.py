from fastapi import Depends

from app.features.balancing.schemas.financial_debt_schema import FinancialDebtFilterSchema, FinancialDebtResponseSchema
from app.features.balancing.services.financial_debt_service import FinancialDebtService
from app.features.balancing.routes.financial_debts.financial_debt_router import financial_debt_router
from app.features.balancing.dependencies.financial_debt.service import get_financial_debt_service

@financial_debt_router.get(
    "",
    response_model=list[FinancialDebtResponseSchema],
)
async def get_financial_debts(
    filters: FinancialDebtFilterSchema = Depends(),
    service: FinancialDebtService = Depends(
        get_financial_debt_service
    ),
):
    result = await service.find(
        balance_snapshot_id=filters.balance_snapshot_id,
        bank_name=filters.bank_name,
        fiscal_year=filters.fiscal_year,
        status=filters.status,
    )

    return result