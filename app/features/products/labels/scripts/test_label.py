from app.features.products.labels.pdf_renderer import (
    LabelPdfRenderer,
)
from app.features.products.labels.dto import LabelDTO
from app.features.products.types import BrandType


label = LabelDTO(
    product_name="BGO. PANT.DRILL SEMI/CH.",
    barcode="GCA6F92KQ1L7T4",
    base_price="149.90",
    brand_type=BrandType.BGOO,
)


renderer = LabelPdfRenderer()

pdf = renderer.render(
    [label]
)


with open(
    "test-label.pdf",
    "wb",
) as file:
    file.write(pdf.read())