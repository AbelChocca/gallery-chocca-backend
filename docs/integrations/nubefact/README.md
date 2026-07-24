# Sistema de Facturación Electrónica - Integración Nubefact

Este módulo se encarga de la integración entre nuestro modelo de base de datos transaccional y la API de **Nubefact** (PSE autorizado por la SUNAT) para la emisión, consulta y anulación de comprobantes de pago electrónicos (Facturas, Boletas, Notas de Crédito y Notas de Débito).

## Arquitectura y Relación con el Modelo de Datos

La integración mapea el estado transaccional de una venta (`sale`) y sus pagos (`payment`) hacia la estructura requerida por Nubefact, registrando la respuesta final de la SUNAT en la tabla `sale_document`.

### Componentes de la Base de Datos Relacionados

- **`customer`**: Contiene la información de identidad del adquirente (DNI, RUC, etc.), la cual se mapea a los campos `cliente_tipo_de_documento`, `cliente_numero_de_documento`, y `cliente_denominacion`.
- **`sale` y `sale_item`**: Representan la cabecera y el detalle de la transacción comercial. Los montos calculados (`subtotal`, `tax`, `total`) se concilian con los totales de Nubefact (`total_gravada`, `total_igv`, `total`).
- **`payment`**: Controla el flujo financiero. Si el método indica condiciones específicas (ej. Crédito), se activa el desglose en el nodo `venta_al_credito` de la API.
- **`sale_document`**: Registra la auditoría completa del comprobante electrónico: enlaces de descarga (PDF, XML, CDR), estado ante SUNAT (`sunat_status`), firma digital (`hash`), y códigos de respuesta.

## Requisitos de Autenticación

Para interactuar con la API (ya sea en su versión ONLINE, OFFLINE o RESELLER), se deben proveer las siguientes cabeceras HTTP en cada solicitud:

```http
Authorization: Bearer <TU_TOKEN_NUBEFACT>
Content-Type: application/json
```

- **RUTA (Endpoint):** Única por cliente o subdominio.
  - _Producción/Demo ONLINE:_ `https://api.nubefact.com/api/v1/<client-uuid>`
  - _Versión OFFLINE:_ `http://localhost:8000/api/v1/<client-uuid>`

## Operaciones Soportadas

El módulo implementa de forma estricta las 4 operaciones principales del API de Nubefact:

1. **Generar Comprobante (`generar_comprobante`)**: Emisión de Facturas, Boletas y Notas asociadas.
2. **Consultar Comprobante (`consultar_comprobante`)**: Verificación del estado actual y recuperación de URLs (PDF, XML, CDR).
3. **Generar Anulación (`generar_anulacion`)**: Comunicación de baja para documentos aceptados.
4. **Consultar Anulación (`consultar_anulacion`)**: Verificación del estado de procesamiento del ticket de baja ante la SUNAT.
