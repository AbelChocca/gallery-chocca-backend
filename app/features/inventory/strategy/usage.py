from app.features.inventory.strategy.sale import (
    SaleStrategy
)

class UsageStrategy(
    SaleStrategy
):
    """
    Returning items to supplier decreases stock.
    """
    pass