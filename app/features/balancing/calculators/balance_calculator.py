from decimal import Decimal


class BalanceCalculator:

    @staticmethod
    def calculate_inventory_total(
        raw_material: Decimal,
        work_in_progress: Decimal,
        finished_goods: Decimal,
    ) -> Decimal:

        return (
            raw_material
            + work_in_progress
            + finished_goods
        )

    @staticmethod
    def calculate_current_assets(
        accounts_receivable: Decimal,
        inventory_valuation: Decimal,
    ) -> Decimal:

        return accounts_receivable + inventory_valuation

    @staticmethod
    def calculate_current_liabilities(
        accounts_payable: Decimal,
        financial_debt: Decimal,
        other_current_liabilities: Decimal,
    ) -> Decimal:

        return (
            accounts_payable
            + financial_debt
            + other_current_liabilities
        )

    @staticmethod
    def calculate_working_capital(
        current_assets: Decimal,
        current_liabilities: Decimal,
    ) -> Decimal:

        return current_assets - current_liabilities


def get_balance_calculator() -> BalanceCalculator:
    return BalanceCalculator()