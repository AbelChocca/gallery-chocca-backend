from enum import Enum



class SaleStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SaleChannel(str, Enum):
    POS = "POS"
    ECOMMERCE = "ECOMMERCE"