from enum import Enum


class ComplaintResponseStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_SEND = "PENDING_SEND"
    SENT = "SENT"
    DELIVERY_FAILED = "DELIVERY_FAILED"