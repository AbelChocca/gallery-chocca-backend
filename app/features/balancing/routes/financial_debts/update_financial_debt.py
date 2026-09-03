from fastapi import Depends, status

from app.features.balancing.schemas.financial_debt_schema import FinancialDebtUpdateSchema
from app.features.balancing.services.financial_debt_service import FinancialDebtService
from app.features.balancing.types.financial_debt_types import FinancialDebtUpdate
from app.features.balancing.routes.financial_debts.financial_debt_router import financial_debt_router
from app.features.balancing.dependencies.financial_debt.service import get_financial_debt_service

@financial_debt_router.put(
    "/{financial_debt_id}",
    status_code=status.HTTP_200_OK,
)
async def update_financial_debt(
    financial_debt_id: int,
    payload: FinancialDebtUpdateSchema,
    service: FinancialDebtService = Depends(get_financial_debt_service),
):
    update_dto = FinancialDebtUpdate(
        bank_name=payload.bank_name,
        amount=payload.amount,
        status=payload.status,
        fields_set=payload.model_fields_set
    )

    return await service.update(
        financial_debt_id,
        update_dto,
    )