from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    YAPE = "YAPE"
    PLIN = "PLIN"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
