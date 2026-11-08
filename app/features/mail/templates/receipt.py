from dataclasses import dataclass
from html import escape


@dataclass
class ReceiptMailTemplateData:
    recipient_name: str
    series_number: str
    document_type: str
    total_amount: str


class ReceiptMailTemplate:

    @staticmethod
    def subject(
        data: ReceiptMailTemplateData,
    ) -> str:
        return (
            f"Has recibido tu "
            f"{data.document_type.lower()} "
            f"{data.series_number}"
        )

    @staticmethod
    def render_html(
        data: ReceiptMailTemplateData,
    ) -> str:

        recipient_name = escape(
            data.recipient_name
        )

        series_number = escape(
            data.series_number
        )

        document_type = escape(
            data.document_type.upper()
        )

        total_amount = escape(
            data.total_amount
        )

        return f"""
        <!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  </head>

  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f3f4f6;
      font-family: Arial, Helvetica, sans-serif;
      color: #111827;
    "
  >
    <table
      role="presentation"
      width="100%"
      cellspacing="0"
      cellpadding="0"
      border="0"
      style="background-color: #f3f4f6; padding: 32px 12px"
    >
      <tr>
        <td align="center">
          <table
            role="presentation"
            width="100%"
            cellspacing="0"
            cellpadding="0"
            border="0"
            style="
              max-width: 700px;
              background-color: #ffffff;
              border: 1px solid #e5e7eb;
            "
          >
            <!-- HEADER -->
            <tr>
              <td
                style="
                  padding: 24px 28px;
                  background-color: #ffffff;
                  border-bottom: 1px solid #e5e7eb;
                "
              >
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                >
                  <tr>
                    <td width="45%" valign="middle" align="left">
                      <img
                        src="https://res.cloudinary.com/ddce1vmuf/image/upload/v1792291240/tkw3sljcgsujjleydowe.png"
                        alt="OLD DENIM CLUB"
                        width="170"
                        style="
                          display: block;
                          width: 170px;
                          max-width: 100%;
                          height: auto;
                          border: 0;
                          outline: none;
                          text-decoration: none;
                        "
                      />
                    </td>

                    <td
                      width="55%"
                      align="right"
                      valign="middle"
                      style="
                        font-size: 13px;
                        line-height: 1.5;
                        color: #6b7280;
                        font-weight: 600;
                      "
                    >
                      Compra fácil, segura y confiable
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- CONTENT -->
            <tr>
              <td style="padding: 36px 28px 28px 28px">
                <p
                  style="
                    margin: 0 0 16px 0;
                    font-size: 20px;
                    font-weight: 700;
                    color: #111827;
                  "
                >
                  Hola {recipient_name},
                </p>

                <p
                  style="
                    margin: 0;
                    font-size: 16px;
                    line-height: 1.8;
                    color: #4b5563;
                  "
                >
                  Has recibido tu
                  <strong style="color: #2563eb">{document_type}</strong>
                  emitida por
                  <strong style="color: #111827">OLD DENIM CLUB</strong>.
                </p>

                <p
                  style="
                    margin: 18px 0 0 0;
                    font-size: 15px;
                    line-height: 1.7;
                    color: #6b7280;
                  "
                >
                  A continuación encontrarás los datos principales de tu
                  comprobante electrónico.
                </p>
              </td>
            </tr>

            <!-- DOCUMENT INFO -->
            <tr>
              <td style="padding: 0 28px 28px 28px">
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                  style="
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                  "
                >
                  <tr>
                    <td style="padding: 24px 26px">
                      <p
                        style="
                          margin: 0 0 18px 0;
                          font-size: 12px;
                          font-weight: 700;
                          letter-spacing: 1px;
                          text-transform: uppercase;
                          color: #64748b;
                        "
                      >
                        Detalle del comprobante
                      </p>

                      <table
                        role="presentation"
                        width="100%"
                        cellspacing="0"
                        cellpadding="0"
                        border="0"
                      >
                        <tr>
                          <td
                            style="
                              padding: 10px 0;
                              width: 46%;
                              color: #64748b;
                              font-size: 14px;
                            "
                          >
                            Nro. {document_type}:
                          </td>

                          <td
                            style="
                              padding: 10px 0;
                              color: #1d4ed8;
                              font-weight: 700;
                              font-size: 15px;
                            "
                          >
                            {series_number}
                          </td>
                        </tr>

                        <tr>
                          <td
                            style="
                              padding: 15px 0 0 0;
                              border-top: 1px solid #e2e8f0;
                              color: #334155;
                              font-weight: 700;
                              font-size: 14px;
                            "
                          >
                            MONTO TOTAL:
                          </td>

                          <td
                            style="
                              padding: 15px 0 0 0;
                              border-top: 1px solid #e2e8f0;
                              color: #2563eb;
                              font-weight: 700;
                              font-size: 20px;
                            "
                          >
                            PEN {total_amount}
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- ATTACHMENTS -->
            <tr>
              <td style="padding: 0 28px 36px 28px">
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                  style="
                    background-color: #eff6ff;
                    border: 1px solid #bfdbfe;
                    border-radius: 8px;
                  "
                >
                  <tr>
                    <td style="padding: 18px 20px">
                      <p
                        style="
                          margin: 0 0 6px 0;
                          font-size: 14px;
                          font-weight: 700;
                          color: #1e40af;
                        "
                      >
                        Tu comprobante está adjunto
                      </p>

                      <p
                        style="
                          margin: 0;
                          font-size: 14px;
                          line-height: 1.7;
                          color: #1e40af;
                        "
                      >
                        Encontrarás los archivos PDF y XML correspondientes a tu
                        comprobante electrónico adjuntos a este correo.
                      </p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- FOOTER -->
            <tr>
              <td
                align="center"
                style="
                  padding: 25px 28px;
                  background-color: #f9fafb;
                  border-top: 1px solid #e5e7eb;
                "
              >
                <p
                  style="
                    margin: 0;
                    font-size: 15px;
                    font-weight: 700;
                    color: #111827;
                  "
                >
                  ¡Gracias por comprar en OLD DENIM CLUB!
                </p>

                <p style="margin: 10px 0 0 0; font-size: 13px; color: #6b7280">
                  Agradecemos tu confianza.
                </p>
              </td>
            </tr>

            <!-- LEGAL -->
            <tr>
              <td
                style="padding: 22px 28px 28px 28px; background-color: #ffffff"
              >
                <p
                  style="
                    margin: 0;
                    font-size: 11px;
                    line-height: 1.7;
                    color: #9ca3af;
                    text-align: center;
                  "
                >
                  Este correo fue enviado automáticamente como confirmación de
                  la emisión de tu comprobante electrónico. Si tienes alguna
                  consulta sobre tu compra o comprobante, comunícate
                  directamente con OLD DENIM CLUB.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""