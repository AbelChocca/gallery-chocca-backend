from typing import Annotated
from datetime import datetime

from fastapi import (
    Depends,
    status,
)
from fastapi.responses import StreamingResponse

from app.features.products.labels.label_route import labels_route

from app.features.products.labels.dto import LabelRequest
from app.features.products.labels.use_cases.generate_product_labels import (
    GenerateProductsLabelsUseCase
)
from app.features.products.labels.dependency import (
    get_generate_products_labels_use_case
)


@labels_route.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Generate products labels PDF",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {
                "application/pdf": {}
            },
            "description": "PDF with generated product labels",
        }
    },
)
async def generate_products_labels(
    requests: list[LabelRequest],
    use_case: Annotated[
        GenerateProductsLabelsUseCase,
        Depends(get_generate_products_labels_use_case),
    ],
):
    pdf = await use_case.execute(requests)

    pdf.seek(0)

    filename = f"product-labels-{datetime.now():%Y%m%d-%H%M%S}.pdf"

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'inline; filename="{filename}"'
            ),
        },
    )