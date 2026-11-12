from abc import ABC, abstractmethod

from app.features.receipts.types.receipt import IssuedReceiptDTO, IssueReceiptDTO, ReceiptAttachmentDTO

class ReceiptProvider(ABC):

    @abstractmethod
    async def issue_receipt(
        self,
        payload: IssueReceiptDTO,
        *,
        idempotency_key: str,
    ) -> IssuedReceiptDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_attachment(
        self,
        *,
        external_id: str,
        attachment_type: str,
        filename: str,
    ) -> ReceiptAttachmentDTO:
        raise NotImplementedError