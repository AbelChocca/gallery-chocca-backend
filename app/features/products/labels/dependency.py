from typing import Annotated

from fastapi import Depends

from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork

from app.features.products.labels.service import LabelService
from app.features.products.labels.pdf_renderer import LabelPdfRenderer
from app.features.products.labels.use_cases.generate_product_labels import (
    GenerateProductsLabelsUseCase
)


def get_label_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> LabelService:
    return LabelService(
        variant_size_repository=uow.variant_sizes,
    )


def get_label_pdf_renderer() -> LabelPdfRenderer:
    return LabelPdfRenderer()


def get_generate_products_labels_use_case(
    label_service: Annotated[
        LabelService,
        Depends(get_label_service),
    ],
    pdf_renderer: Annotated[
        LabelPdfRenderer,
        Depends(get_label_pdf_renderer),
    ],
) -> GenerateProductsLabelsUseCase:
    return GenerateProductsLabelsUseCase(
        label_service=label_service,
        label_pdf_renderer=pdf_renderer,
    )