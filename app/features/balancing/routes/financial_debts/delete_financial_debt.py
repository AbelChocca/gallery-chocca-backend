from fastapi import Depends, status

from app.features.balancing.services.financial_debt_service import FinancialDebtService
from app.features.balancing.routes.financial_debts.financial_debt_router import financial_debt_router
from app.features.balancing.dependencies.financial_debt.service import get_financial_debt_service

@financial_debt_router.delete(
    "/{financial_debt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_financial_debt(
    financial_debt_id: int,
    service: FinancialDebtService = Depends(
        get_financial_debt_service
    ),
) -> None:
    await service.delete(financial_debt_id)