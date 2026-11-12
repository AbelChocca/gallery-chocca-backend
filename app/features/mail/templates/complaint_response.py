
from dataclasses import dataclass
from html import escape


@dataclass(frozen=True, slots=True)
class ComplaintResponseMailTemplateData:
    recipient_name: str
    complaint_number: str
    message: str
    provider_name: str


class ComplaintResponseMailTemplate:

    @staticmethod
    def subject(
        data: ComplaintResponseMailTemplateData,
    ) -> str:
        return (
            "CHOCCA | Respuesta a tu reclamación "
            f"{data.complaint_number}"
        )

    @staticmethod
    def render_html(
        data: ComplaintResponseMailTemplateData,
    ) -> str:

        name = escape(data.recipient_name)
        number = escape(data.complaint_number)
        provider = escape(data.provider_name)

        message = escape(data.message).replace(
            "\n", "<br />"
        )

        return f"""
        <!doctype html>
        <html lang="es">
          <head>
            <meta charset="UTF-8" />
          </head>

          <body style="
            margin:0;
            padding:32px 12px;
            background:#f3f4f6;
            font-family:Arial,Helvetica,sans-serif;
            color:#171717;
          ">
            <table role="presentation"
                   width="100%"
                   cellspacing="0"
                   cellpadding="0"
                   style="
                     max-width:640px;
                     margin:auto;
                     background:#ffffff;
                   ">
              <tr>
                <td style="
                  padding:28px 32px;
                  background:#071a35;
                  color:#ffffff;
                ">
                  <p style="
                    margin:0;
                    font-size:13px;
                    letter-spacing:2px;
                  ">CHOCCA</p>

                  <h1 style="
                    margin:18px 0 0;
                    font-size:24px;
                  ">Respuesta a tu reclamación</h1>
                </td>
              </tr>

              <tr>
                <td style="padding:32px;">
                  <p>Estimado/a {name}:</p>

                  <p style="
                    color:#64748b;
                    font-size:14px;
                    line-height:1.7;
                  ">
                    En atención a la reclamación
                    <strong>{number}</strong>,
                    te comunicamos nuestra respuesta:
                  </p>

                  <div style="
                    padding:24px;
                    background:#f8fafc;
                    border-left:3px solid #3863A0;
                    font-size:15px;
                    line-height:1.9;
                    overflow-wrap:break-word;
                  ">
                    {message}
                  </div>

                  <p style="
                    margin-top:28px;
                    line-height:1.7;
                  ">
                    Atentamente,<br />
                    <strong>{provider}</strong>
                  </p>
                </td>
              </tr>

              <tr>
                <td style="
                  padding:20px 32px;
                  border-top:1px solid #e2e8f0;
                  color:#64748b;
                  font-size:12px;
                ">
                  Comunicación formal del Libro de
                  Reclamaciones de CHOCCA.
                </td>
              </tr>
            </table>
          </body>
        </html>
        """
