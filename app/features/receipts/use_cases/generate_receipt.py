from decimal import Decimal

from app.core.exceptions import InvalidOperation

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.services.order_billing_service import (
    OrderBillingService,
)
from app.features.orders.services.order_item_service import (
    OrderItemService,
)
from app.features.orders.services.order_receipt import (
    OrderReceiptService,
)

from app.features.orders.types.order import (
    OrderStatus,
)

from app.features.receipts.types.receipt import (
    IssueReceiptDTO,
    IssuedReceiptDTO,
    ReceiptItemDTO,
    ReceiptCustomerDTO,
)

from app.features.receipts.services.receipt_service import (
    ReceiptService,
)

from app.features.receipts.exceptions import (
    ReceiptProviderInsufficientCredits,
    ReceiptProviderInvalidRequest,
)
from app.features.mail.services.mail_service import (
    MailService,
)
from app.features.mail.types.mail import (
    SendMailDTO,
    MailAttachmentDTO
)
from app.features.mail.exceptions import (
    MailProviderError,
)
from app.features.mail.templates.receipt import (
    ReceiptMailTemplate,
    ReceiptMailTemplateData,
)

class GenerateReceiptUseCase:

    def __init__(
        self,
        *,
        order_service: OrderService,
        order_billing_service: OrderBillingService,
        order_item_service: OrderItemService,
        order_receipt_service: OrderReceiptService,
        receipt_service: ReceiptService,
        mail_service: MailService,
    ) -> None:

        self._order_service = order_service
        self._order_billing_service = (
            order_billing_service
        )
        self._order_item_service = (
            order_item_service
        )
        self._order_receipt_service = (
            order_receipt_service
        )
        self._receipt_service = (
            receipt_service
        )
        self._mail_service = (
            mail_service
        )

    async def execute(
        self,
        *,
        order_id: int,
        send_to_mail: bool = True,
    ) -> IssuedReceiptDTO:

        order = await self._order_service.get_by_id(
            order_id=order_id,
            raises=True,
            with_lock=True,
        )

        if order.id is None:
            raise InvalidOperation(
                message=(
                    "El pedido no tiene un "
                    "identificador válido."
                ),
            )

        if order.status in {
            OrderStatus.PENDING_PAYMENT,
            OrderStatus.PENDING_SHIPPING_QUOTE,
            OrderStatus.CANCELLED,
        }:
            raise InvalidOperation(
                message=(
                    "El pedido todavía no está listo "
                    "para emitir un comprobante."
                ),
            )

        billing = (
            await self._order_billing_service
            .get_by_order_id(
                order_id=order.id,
                raises=True,
            )
        )

        order_items = (
            await self._order_item_service
            .get_by_order_id(
                order_id=order.id,
            )
        )

        if not order_items:
            raise InvalidOperation(
                message=(
                    "El pedido no contiene productos "
                    "para emitir el comprobante."
                ),
            )

        order_receipt = (
            await self._order_receipt_service
            .get_by_order_id(
                order_id=order.id,
                raises=False,
                with_lock=True,
            )
        )

        if order_receipt is None:
            order_receipt = (
                await self._order_receipt_service
                .create(
                    order_id=order.id,
                    flush=True,
                )
            )

        if order_receipt.id is None:
            raise InvalidOperation(
                message=(
                    "El comprobante del pedido no "
                    "tiene un identificador válido."
                ),
            )

        if order_receipt.is_issued:
            raise InvalidOperation(
                message=(
                    "El pedido ya tiene un "
                    "comprobante emitido."
                ),
            )

        await self._order_receipt_service.mark_as_issuing(
            receipt=order_receipt,
            flush=True,
        )

        receipt_items = [
            ReceiptItemDTO(
                sku=item.sku,
                description=(
                    self._build_item_description(
                        item=item,
                    )
                ),
                quantity=Decimal(
                    str(item.quantity)
                ),
                unit_price=item.unit_final_price,
            )
            for item in order_items
        ]

        if order.shipping_cost > Decimal("0.00"):
            receipt_items.append(
                ReceiptItemDTO(
                    sku="SHIPPING",
                    description="Servicio de envío",
                    quantity=Decimal("1"),
                    unit_price=order.shipping_cost,
                )
            )

        payload = IssueReceiptDTO(
            receipt_type=(
                billing.document_type
            ),
            customer=ReceiptCustomerDTO(
                document_type=(
                    billing.identity_document_type
                ),
                document_number=(
                    billing.identity_document_number
                ),
            ),
            items=receipt_items,
            currency="PEN",
        )

        try:
            result = await self._receipt_service.issue(
                payload=payload,
                idempotency_key=(
                    f"order-receipt-"
                    f"{order_receipt.id}"
                ),
            )

        except ReceiptProviderInsufficientCredits as exc:
            await (
                self._order_receipt_service
                .mark_as_retry_pending(
                    receipt=order_receipt,
                    provider_error_code=(
                        exc.error_code
                    ),
                    provider_error_message=(
                        str(exc)
                    ),
                    flush=True,
                )
            )

            raise

        except ReceiptProviderInvalidRequest as exc:
            await (
                self._order_receipt_service
                .mark_as_failed(
                    receipt=order_receipt,
                    provider_error_code=(
                        exc.error_code
                    ),
                    provider_error_message=(
                        str(exc)
                    ),
                    flush=True,
                )
            )

            raise

        if result.accepted_by_sunat:
            order_receipt = await (
                self._order_receipt_service
                .mark_as_issued(
                    receipt=order_receipt,
                    external_id=result.external_id,
                    series_number=(
                        result.series_number
                    ),
                    flush=True,
                )
            )

        else:
            await (
                self._order_receipt_service
                .mark_as_retry_pending(
                    receipt=order_receipt,
                    external_id=result.external_id,
                    series_number=(
                        result.series_number
                    ),
                    provider_error_code=(
                        result.sunat_code
                    ),
                    provider_error_message=(
                        result.sunat_description
                    ),
                    flush=True,
                )
            )

        if (
            send_to_mail
            and result.accepted_by_sunat
        ):
            try:
                pdf_attachment = (
                    await self._receipt_service
                    .get_attachment(
                        external_id=result.external_id,
                        attachment_type="pdf",
                        filename=(
                            f"{result.series_number}.pdf"
                        ),
                    )
                )

                xml_attachment = (
                    await self._receipt_service
                    .get_attachment(
                        external_id=result.external_id,
                        attachment_type="xml",
                        filename=(
                            f"{result.series_number}.xml"
                        ),
                    )
                )

                mail_data = ReceiptMailTemplateData(
                    recipient_name=billing.recipient_name,
                    series_number=result.series_number,
                    document_type=(
                        billing.document_type.value
                    ),
                    total_amount=str(order.total),
                )

                sent_mail = await self._mail_service.send(
                    payload=SendMailDTO(
                        to=billing.email,
                        subject=(
                            ReceiptMailTemplate.subject(
                                mail_data
                            )
                        ),
                        html=(
                            ReceiptMailTemplate.render_html(
                                mail_data
                            )
                        ),
                        attachments=[
                            MailAttachmentDTO(
                                filename=pdf_attachment.filename,
                                content=pdf_attachment.content,
                            ),
                            MailAttachmentDTO(
                                filename=xml_attachment.filename,
                                content=xml_attachment.content,
                            ),
                        ],
                    )
                )

                await (
                    self._order_receipt_service
                    .mark_email_sent(
                        receipt=order_receipt,
                        provider_id=sent_mail.id,
                        flush=True,
                    )
                )

            except MailProviderError as exc:
                await (
                    self._order_receipt_service
                    .mark_email_failed(
                        receipt=order_receipt,
                        error_message=str(exc),
                        flush=True,
                    )
                )

        return result

    @staticmethod
    def _build_item_description(
        *,
        item,
    ) -> str:

        details: list[str] = []

        if item.color:
            details.append(
                f"Color: {item.color}"
            )

        if item.size:
            details.append(
                f"Talla: {item.size}"
            )

        if not details:
            return item.product_name

        return (
            f"{item.product_name} "
            f"({' - '.join(details)})"
        )