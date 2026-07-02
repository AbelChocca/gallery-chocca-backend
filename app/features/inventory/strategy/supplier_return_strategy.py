from app.features.inventory.strategy.sale import (
    SaleStrategy
)

class SupplierReturnStrategy(
    SaleStrategy
):
    """
    Returning items to supplier decreases stock.
    """
    pass