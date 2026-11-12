from enum import Enum

class BillingDocumentType(str, Enum):
    RECEIPT = "BOLETA"
    INVOICE = "FACTURA"