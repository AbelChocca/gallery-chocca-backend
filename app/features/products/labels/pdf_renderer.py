from io import BytesIO

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.features.products.labels.dto import LabelDTO
from app.features.products.labels.helpers.brand_assets import (
    BrandAssets,
)
from reportlab.lib.colors import HexColor
from reportlab.graphics.barcode import code128
from app.features.products.types import BrandType

pdfmetrics.registerFont(TTFont('Oswald-Regular', 'app/assets/fonts/Oswald-Regular.ttf'))



LABEL_WIDTH = 50 * mm
LABEL_HEIGHT = 30 * mm
MAX_WIDTH = 42 * mm
LABEL_BLUE = HexColor("#112D65")

class LabelPdfRenderer:

    def __init__(self):
        self.logos = {
            BrandType.BGOO: BrandAssets.logo(BrandType.BGOO),
            BrandType.AMD: BrandAssets.logo(BrandType.AMD),
        }

    def render(
        self,
        labels: list[LabelDTO],
    ) -> BytesIO:

        buffer = BytesIO()

        pdf = canvas.Canvas(
            buffer,
            pagesize=(
                LABEL_WIDTH,
                LABEL_HEIGHT,
            ),
        )

        for label in labels:
            self._draw_label(
                pdf,
                label,
            )

            pdf.showPage()

        pdf.save()

        buffer.seek(0)

        return buffer


    def _draw_label(
        self,
        pdf: canvas.Canvas,
        label: LabelDTO,
    ) -> None:

        pdf.setFillColor(LABEL_BLUE)

        # 1. Dibujar el Logo en la parte superior
        self._draw_logo(
            pdf,
            label,
        )

        # Definimos el centro del bloque izquierdo (aprox 19mm) para alinear textos
        center_x = 17.8 * mm

        # 2. Nombre del producto (Debajo del logo)
        pdf.setFont("Oswald-Regular", 8.5)


        name = label.product_name

        if pdfmetrics.stringWidth(name, "Helvetica-Bold", 8.5) <= MAX_WIDTH:
            pdf.drawCentredString(center_x, 13 * mm, name, wordSpace=0.8)
        else:
            # Lo dividimos en dos líneas
            words = name.split()

            line1 = ""
            line2 = ""

            for word in words:
                test = f"{line1} {word}".strip()

                if pdfmetrics.stringWidth(test, "Helvetica-Bold", 8.5) <= MAX_WIDTH:
                    line1 = test
                else:
                    line2 = f"{line2} {word}".strip()

            pdf.drawCentredString(center_x, 13.7 * mm, line1)
            pdf.drawCentredString(center_x, 11 * mm, line2)

        # 3. Precio sugerido y Valor
        if label.base_price:
            pdf.setFont("Helvetica", 8)
            pdf.drawCentredString(
                center_x,
                7.3 * mm,
                "Precio sugerido:",
            )
            
            # Precio más grande y en negrita
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(
                center_x,
                2.8 * mm,
                f"S/ {label.base_price}",
            )

        # 4. Código de barras (Lado derecho)
        self._draw_barcode(
            pdf,
            label,
        )


    def _draw_logo(
        self,
        pdf: canvas.Canvas,
        label: LabelDTO,
    ) -> None:

        logo_path = self.logos[label.brand_type]

        if not logo_path.exists():
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawCentredString(
                18 * mm, 
                22 * mm, 
                label.brand_type.value
            )
            return

        width = 34 * mm

        if label.brand_type == BrandType.AMD:
            width = 36 * mm

        x = 1 * mm
        
        if label.brand_type == BrandType.AMD:
            x = 0.75 * mm

        # Ajustamos dimensiones para que ocupe bien la parte superior izquierda
        pdf.drawImage(
            str(logo_path),
            x,      # Margen izquierdo
            17 * mm,     # Posición Y (hacia arriba)
            width=width,
            height=11 * mm,
            preserveAspectRatio=True,
            mask="auto",
        )

    def _draw_barcode(
        self,
        pdf: canvas.Canvas,
        label: LabelDTO,
    ) -> None:

        # Configuramos el código de barras más grueso para que coincida con la imagen
        barcode = code128.Code128(
            label.barcode,
            barHeight=10 * mm,  # Al rotar, esto será el ancho que ocupa de izquierda a derecha
            barWidth=0.133 * mm, # Grosor de las barras
            barFillColor=LABEL_BLUE,
            humanReadable=True,
        )

        pdf.saveState()

        # Nos movemos a la derecha (dejando 2mm de margen derecho) y 3mm de margen inferior
        pdf.translate(
            45.3 * mm,
            -3.7 * mm,
        )

        pdf.rotate(90)

        # Dibujamos en (0,0) relativo a la nueva rotación
        barcode.drawOn(
            pdf,
            0,
            0,
        )

        pdf.restoreState()