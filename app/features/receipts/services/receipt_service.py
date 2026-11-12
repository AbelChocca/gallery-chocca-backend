from app.features.receipts.providers.base import (
    ReceiptProvider,
    IssueReceiptDTO,
    IssuedReceiptDTO,
    ReceiptAttachmentDTO
)

class ReceiptService:

    def __init__(
        self,
        provider: ReceiptProvider,
    ) -> None:
        self._provider = provider

    async def get_attachment(
        self,
        *,
        external_id: str,
        attachment_type: str,
        filename: str,
    ) -> ReceiptAttachmentDTO:

        return await self._provider.get_attachment(
            external_id=external_id,
            attachment_type=attachment_type,
            filename=filename,
        )

    async def issue(
        self,
        *,
        payload: IssueReceiptDTO,
        idempotency_key: str,
    ) -> IssuedReceiptDTO:

        return await self._provider.issue_receipt(
            payload,
            idempotency_key=idempotency_key,
        )