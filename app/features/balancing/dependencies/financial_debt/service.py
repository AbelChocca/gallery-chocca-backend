from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.balancing.services.financial_debt_service import FinancialDebtService

from fastapi import Depends


def get_financial_debt_service(
    uow: UnitOfWork = Depends(get_uow),
) -> FinancialDebtService:

    return FinancialDebtService(
        financial_debt_repository=uow.financial_debts,
    )