from dataclasses import dataclass
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True)
class ComplaintReceiptMailTemplateData:
    recipient_name: str
    complaint_number: str
    complaint_type: str
    created_at: datetime


class ComplaintReceiptMailTemplate:

    @staticmethod
    def subject(
        data: ComplaintReceiptMailTemplateData,
    ) -> str:
        return (
            "CHOCCA | Constancia de "
            f"{data.complaint_type.lower()} "
            f"{data.complaint_number}"
        )

    @staticmethod
    def render_html(
        data: ComplaintReceiptMailTemplateData,
    ) -> str:
        name = escape(data.recipient_name)
        number = escape(data.complaint_number)
        complaint_type = escape(
            data.complaint_type.capitalize()
        )

        local_date = (
            data.created_at
            .astimezone(ZoneInfo("America/Lima"))
            .strftime("%d/%m/%Y %H:%M")
        )

        return f"""
        <!doctype html>
        <html lang="es">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0" />
          </head>

          <body style="
            margin:0;
            padding:32px 12px;
            background:#f3f4f6;
            font-family:Arial,Helvetica,sans-serif;
            color:#171717;
          ">
            <table role="presentation"
                   cellspacing="0"
                   cellpadding="0"
                   width="100%"
                   style="
                     max-width:640px;
                     margin:0 auto;
                     background:#ffffff;
                     border-collapse:collapse;
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
                    font-weight:700;
                  ">CHOCCA</p>

                  <h1 style="
                    margin:18px 0 0;
                    font-size:25px;
                    line-height:1.3;
                  ">
                    Reclamación registrada
                  </h1>
                </td>
              </tr>

              <tr>
                <td style="padding:36px 32px;">
                  <p style="
                    margin:0 0 16px;
                    font-size:18px;
                    font-weight:700;
                  ">Hola, {name}</p>

                  <p style="
                    font-size:15px;
                    line-height:1.8;
                    color:#475569;
                  ">
                    Hemos registrado tu {complaint_type.lower()}
                    en el Libro de Reclamaciones de
                    OLD DENIM CLUB.
                  </p>

                  <table role="presentation"
                         width="100%"
                         style="
                           margin:28px 0;
                           background:#f8fafc;
                           border:1px solid #e2e8f0;
                         ">
                    <tr>
                      <td style="padding:24px;">
                        <p style="
                          margin:0 0 8px;
                          color:#64748b;
                          font-size:12px;
                        ">NÚMERO DE RECLAMACIÓN</p>

                        <p style="
                          margin:0;
                          color:#071a35;
                          font-size:26px;
                          font-weight:700;
                        ">{number}</p>

                        <p style="
                          margin:16px 0 0;
                          font-size:13px;
                          color:#475569;
                        ">
                          Tipo: {complaint_type}<br />
                          Registro: {local_date} (Perú)
                        </p>
                      </td>
                    </tr>
                  </table>

                  <p style="
                    font-size:14px;
                    line-height:1.8;
                    color:#475569;
                  ">
                    Nuestro equipo revisará tu solicitud.
                    El plazo máximo de atención es de
                    15 días hábiles.
                  </p>

                  <p style="
                    font-size:14px;
                    line-height:1.8;
                    color:#475569;
                  ">
                    Conserva este número para futuras
                    consultas.
                  </p>

                  <p style="
                    margin-top:28px;
                    font-size:14px;
                  ">
                    Atentamente,<br />
                    <strong>OLD DENIM CLUB</strong>
                  </p>
                </td>
              </tr>

              <tr>
                <td style="
                  padding:22px 32px;
                  background:#f8fafc;
                  border-top:1px solid #e2e8f0;
                  text-align:center;
                  font-size:12px;
                  line-height:1.7;
                  color:#64748b;
                ">
                  Libro de Reclamaciones de CHOCCA<br />
                  Este correo confirma el registro;
                  no constituye una resolución del caso.
                </td>
              </tr>
            </table>
          </body>
        </html>
        """