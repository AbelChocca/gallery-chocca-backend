# Gestión de Errores y Códigos de Estado

El sistema debe interceptar y procesar tanto los errores a nivel de protocolo HTTP como los códigos internos devueltos en la capa de negocio de Nubefact para asegurar la resiliencia de la facturación.

## 1. Códigos de Error Propios de Nubefact

Cuando la API devuelve un código HTTP `400` o `200` con un formato erróneo, el cuerpo de la respuesta incluye un objeto con la estructura `{"errors": "Descripción", "codigo": XX}`. Se deben mapear bajo la siguiente lógica:

|   Código    | Descripción Interna                                                    | Acción Recomendada por el Sistema                                                                                                           |
| :---------: | :--------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
|   **10**    | No se pudo autenticar, token incorrecto o eliminado                    | **Alerta Crítica:** Notificar al administrador del sistema de forma inmediata. Detener cola de envíos.                                      |
|   **11**    | La ruta o URL que estás usando no es correcta o no existe              | **Alerta Crítica:** Verificar configuración del Tenant / Endpoint en variables de entorno.                                                  |
|   **12**    | Solicitud incorrecta, la cabecera no contiene un Content-Type correcto | **Bug de Software:** Verificar que el cliente HTTP inyecte `application/json`.                                                              |
|   **20**    | El archivo enviado no cumple con el formato establecido                | **Error de Validación:** El JSON está mal construido o contiene tipos de datos inválidos (ej. comillas sin escapar).                        |
|   **21**    | No se pudo completar la operación (acompaña mensaje específico)        | **Validación SUNAT / Regocio:** Analizar el mensaje adjunto (ej. RUC inactivo, importes descuadrados). Modificar datos antes de reintentar. |
|   **22**    | Documento enviado fuera del plazo permitido                            | **Error de Negocio:** La fecha de emisión sobrepasa los días permitidos por SUNAT para su envío retroactivo.                                |
|   **23**    | Este documento ya existe en NubeFacT                                   | **Duplicidad:** El documento con esa serie y número ya fue emitido. Actualizar el estado local a `COMPLETED` y recuperar los enlaces.       |
|   **24**    | El documento indicado no existe o no fue enviado a NubeFacT            | **Error de Consulta:** Se intentó consultar o anular un comprobante que no tiene registro previo en el PSE.                                 |
|   **40**    | Error interno desconocido                                              | **Reintento Exponencial:** Falla temporal en los servidores de Nubefact. Reintentar la operación más tarde.                                 |
| **50 / 51** | Cuenta suspendida / Falta de pago                                      | **Bloqueo Comercial:** Notificar al equipo administrativo para regularizar el estado comercial con el proveedor.                            |

## 2. Códigos de Estado HTTP

- **`200 OK`**: La solicitud fue procesada por la API de Nubefact. Ojo: Un estado 200 no garantiza aprobación SUNAT; se debe evaluar el campo booleano `aceptada_por_sunat`.
- **`400 Bad Request`**: Malformación estructural del JSON o errores en los parámetros obligatorios de la cabecera.
- **`401 Unauthorized`**: Falla en la validación de la cabecera `Authorization`. Token expirado o mal copiado.
- **`500 Internal Server Error`**: Caída del servicio del PSE o interrupción en el Web Service de la SUNAT.

## 3. Política de Almacenamiento en `sale_document`

Frente a una respuesta de error, se deben poblar los siguientes campos de la tabla local para permitir auditoría y soporte:

- **`sunat_response_code`**: Guarda el código retornado por Nubefact o la SUNAT (`sunat_responsecode`).
- **`sunat_description`**: Almacena el texto descriptivo del rechazo de la SUNAT.
- **`sunat_soap_error`**: Captura los errores de transporte de protocolo o indisponibilidad del servicio de contingencia.
