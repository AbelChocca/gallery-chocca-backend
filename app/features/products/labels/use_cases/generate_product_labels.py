from io import BytesIO

from app.features.products.labels.service import LabelService
from app.features.products.labels.pdf_renderer import LabelPdfRenderer
from app.features.products.labels.dto import LabelRequest
from app.core.exceptions import ValidationError

MAX_PRODUCTS = 50
MAX_COPIES_PER_PRODUCT = 100
MAX_TOTAL_COPIES = 1000

class GenerateProductsLabelsUseCase:

    def __init__(
        self,
        label_service: LabelService,
        label_pdf_renderer: LabelPdfRenderer,
    ):
        self.label_service = label_service
        self.label_pdf_renderer = label_pdf_renderer

    async def execute(
        self,
        requests: list[LabelRequest],
    ) -> BytesIO:
        self._validate_requests(requests)

        labels = await self.label_service.get_many_labels(
            [
                request.variant_size_id
                for request in requests
            ]
        )

        labels_by_id = {
            label.variant_size_id: label
            for label in labels
        }

        missing = {
            request.variant_size_id
            for request in requests
        } - labels_by_id.keys()

        if missing:
            raise ValidationError(
                f"No se encontraron las variantes: {sorted(missing)}"
            )

        labels_to_render = [
            labels_by_id[request.variant_size_id]
            for request in requests
            for _ in range(request.quantity)
        ]

        return self.label_pdf_renderer.render(
            labels_to_render
        )

    def _validate_requests(
        self,
        requests: list[LabelRequest],
    ) -> None:
        if len(requests) > MAX_PRODUCTS:
            raise ValueError(
                f"Solo se permiten hasta {MAX_PRODUCTS} prendas por solicitud."
            )

        total_copies = 0

        for request in requests:
            if request.quantity < 1:
                raise ValidationError(
                    "La cantidad de copias debe ser mayor que cero."
                )

            if request.quantity > MAX_COPIES_PER_PRODUCT:
                raise ValidationError(
                    f"Solo se permiten hasta {MAX_COPIES_PER_PRODUCT} copias por prenda."
                )

            total_copies += request.quantity

        if total_copies > MAX_TOTAL_COPIES:
            raise ValidationError(
                f"Solo se permiten hasta {MAX_TOTAL_COPIES} copias en total."
            )