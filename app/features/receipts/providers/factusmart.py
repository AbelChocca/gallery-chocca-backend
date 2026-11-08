import asyncio
from typing import Any

import factusmart

from app.core.settings.pydantic_settings import settings

from app.features.receipts.providers.base import (
    ReceiptProvider,
)
from app.features.receipts.types.receipt import (
    IssuedReceiptDTO,
    IssueReceiptDTO,
    ReceiptAttachmentDTO
)
from app.features.receipts.types.factusmart import (
    FactuSmartIssueResponseDTO,
    FactuSmartSunatDTO,
)
from app.features.receipts.exceptions import (
    ReceiptProviderInsufficientCredits,
    ReceiptProviderInvalidRequest,
    ReceiptProviderError
)
from app.features.receipts.types.document import (
    BillingDocumentType,
)
from app.features.customer.customer_types import IdentityDocumentType

class FactuSmartReceiptProvider(ReceiptProvider):

    def __init__(self) -> None:
        self._client = factusmart.Cliente(
            api_key=settings.FACTUSMART_API_KEY,
            base_url=(
                f"{settings.FACTUSMART_BASE_URL.rstrip('/')}"
                "/api/v1/issuer"
            ),
            ruc=settings.FACTUSMART_RUC,
            timeout=60,
            max_reintentos=3,
        )

    async def get_attachment(
        self,
        *,
        external_id: str,
        attachment_type: str,
        filename: str,
    ) -> ReceiptAttachmentDTO:

        content = await asyncio.to_thread(
            self._download_attachment_sync,
            external_id,
            attachment_type,
        )

        return ReceiptAttachmentDTO(
            filename=filename,
            content=content,
        )

    async def issue_receipt(
        self,
        payload: IssueReceiptDTO,
        *,
        idempotency_key: str,
    ) -> IssuedReceiptDTO:

        return await asyncio.to_thread(
            self._issue_receipt_sync,
            payload,
            idempotency_key,
        )

    def _issue_receipt_sync(
        self,
        payload: IssueReceiptDTO,
        idempotency_key: str,
    ) -> IssuedReceiptDTO:

        try:
            factusmart_payload = self._build_payload(
                payload
            )

            response = (
                self._client
                .comprobantes
                .emitir(
                    factusmart_payload,
                    idempotency_key=idempotency_key,
                )
            )

        except factusmart.SinCreditos as exc:
            raise ReceiptProviderInsufficientCredits(
                message=(
                    "FactuSmart no tiene suficientes "
                    "créditos."
                ),
                context={
                    "provider": "factusmart",
                    "code": exc.codigo,
                    "retryable": exc.reintentable,
                    "response": exc.respuesta,
                },
            ) from exc

        except factusmart.ErrorDeValidacion as exc:
            raise ReceiptProviderInvalidRequest(
                message=(
                    "FactuSmart rechazó los datos "
                    "del comprobante."
                ),
                context={
                    "provider": "factusmart",
                    "code": exc.codigo,
                    "retryable": exc.reintentable,
                    "response": exc.respuesta,
                },
            ) from exc

        except factusmart.FactuSmartError as exc:
            raise ReceiptProviderError(
                message=(
                    "Ocurrió un error al comunicarse "
                    "con FactuSmart."
                ),
                context={
                    "provider": "factusmart",
                    "code": getattr(exc, "codigo", None),
                    "retryable": getattr(
                        exc,
                        "reintentable",
                        None,
                    ),
                    "response": getattr(
                        exc,
                        "respuesta",
                        None,
                    ),
                },
            ) from exc

        provider_response = self._parse_response(
            response
        )

        return self._to_domain_response(
            provider_response
        )

    def _download_attachment_sync(
        self,
        external_id: str,
        attachment_type: str,
    ) -> bytes:

        return self._client.comprobantes.descargar(
            external_id,
            attachment_type,
        )

    def _build_payload(
        self,
        payload: IssueReceiptDTO,
    ) -> dict[str, Any]:

        calculation = (
            self._client
            .comprobantes
            .calcular(
                self._build_calculation_items(
                    payload
                )
            )
        )

        return {
            "codigo_tipo_documento":
                self._map_receipt_type(
                    payload.receipt_type
                ),

            "datos_del_cliente_o_receptor": {
                "codigo_tipo_documento_identidad":
                    self._map_identity_document_type(
                        payload.customer.document_type
                    ),

                "numero_documento":
                    payload.customer.document_number,
            },

            "items": calculation["items"],
            "totales": calculation["totales"],
        }

    @staticmethod
    def _build_calculation_items(
        payload: IssueReceiptDTO,
    ) -> list[dict[str, Any]]:

        return [
            {
                "codigo_interno": item.sku,
                "descripcion": item.description,
                "unidad_de_medida": "NIU",
                "cantidad": float(item.quantity),

                # Precio FINAL con IGV incluido
                "precio_unitario": float(item.unit_price),

                # Gravado con IGV 18 %
                "afectacion": "10",
            }
            for item in payload.items
        ]

    @staticmethod
    def _map_receipt_type(
        receipt_type: BillingDocumentType,
    ) -> str:

        mapping = {
            BillingDocumentType.RECEIPT: "03",
            BillingDocumentType.INVOICE: "01",
        }

        try:
            return mapping[receipt_type]

        except KeyError as exc:
            raise ValueError(
                f"Unsupported receipt type: "
                f"{receipt_type}"
            ) from exc

    @staticmethod
    def _map_identity_document_type(
        document_type: IdentityDocumentType,
    ) -> str:

        mapping = {
            IdentityDocumentType.DNI: "1",
            IdentityDocumentType.RUC: "6",
        }

        try:
            return mapping[document_type]

        except KeyError as exc:
            raise ValueError(
                "Unsupported identity "
                f"document type: {document_type}"
            ) from exc

    @staticmethod
    def _parse_response(
        data: dict,
    ) -> FactuSmartIssueResponseDTO:

        sunat_data = data.get("sunat")

        sunat = None

        if sunat_data:
            sunat = FactuSmartSunatDTO(
                codigo=sunat_data.get("codigo"),
                descripcion=(
                    sunat_data.get("descripcion")
                ),
            )

        return FactuSmartIssueResponseDTO(
            success=data["success"],

            estado=data["estado"],
            estado_descripcion=(
                data["estado_descripcion"]
            ),

            serie_numero=data["serie_numero"],
            external_id=data["external_id"],

            aceptado_por_sunat=(
                data["aceptado_por_sunat"]
            ),

            sunat=sunat,

            entorno=data.get("entorno"),

            tiene_validez_fiscal=data.get(
                "tiene_validez_fiscal",
                False,
            ),

            creditos_restantes=data.get(
                "creditos_restantes"
            ),
        )

    @staticmethod
    def _to_domain_response(
        response: FactuSmartIssueResponseDTO,
    ) -> IssuedReceiptDTO:

        return IssuedReceiptDTO(
            external_id=response.external_id,
            series_number=response.serie_numero,

            status=response.estado,
            status_description=(
                response.estado_descripcion
            ),

            accepted_by_sunat=(
                response.aceptado_por_sunat
            ),

            sunat_code=(
                response.sunat.codigo
                if response.sunat
                else None
            ),

            sunat_description=(
                response.sunat.descripcion
                if response.sunat
                else None
            ),

            environment=response.entorno,

            has_fiscal_validity=(
                response.tiene_validez_fiscal
            ),

            remaining_credits=(
                response.creditos_restantes
            ),
        )