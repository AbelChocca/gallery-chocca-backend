from abc import ABC, abstractmethod
from decimal import Decimal

class BasePricingStrategy(ABC):

    @abstractmethod
    def apply(
        self,
        *,
        current_price: Decimal,
        value: Decimal
    ) -> Decimal:
        pass

    @abstractmethod
    def validate(
        self,
        value: Decimal
    ) -> None:
        pass