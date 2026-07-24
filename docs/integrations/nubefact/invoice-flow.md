# Flujo de Emisión de Comprobantes Electrónicos

Este documento describe la secuencia lógica y el mapeo de datos requerido para transformar una venta local en un comprobante electrónico válido ante la SUNAT a través de Nubefact.

## Diagrama Secuencial del Proceso

1. **Persistencia Local:** Se crea el registro de la venta en `sale` y sus ítems en `sale_item` con estado `status = 'PENDING'`.
2. **Construcción del Payload JSON:** Se extraen los datos del cliente (`customer`), la venta y sus ítems para armar la estructura solicitada por Nubefact.
3. **Consumo del Servicio:** Se realiza una petición HTTP POST hacia la RUTA configurada enviando el Token en las cabeceras.
4. **Procesamiento de Respuesta:**
   - **Caso Exitoso (200 OK y `aceptada_por_sunat` = true):** Se crea el registro en `sale_document` guardando los enlaces, hash y código QR. El estado de la venta cambia a `COMPLETED`.
   - **Caso Rechazado/Error:** Se almacena el error en `sunat_soap_error` o `sunat_description` dentro de `sale_document` para su posterior subsanación.

## Mapeo Detallado de Datos (Base de Datos ➔ JSON Nubefact)

### 1. Cabecera del Documento

| Campo Base de Datos (`sale` / `customer`) | Campo JSON Nubefact           | Regla de Transformación / Observaciones                            |
| :---------------------------------------- | :---------------------------- | :----------------------------------------------------------------- |
| `sale.id` + `sale.code`                   | `codigo_unico`                | Identificador único opcional para evitar duplicidad en reintentos. |
| `sale_document_type`                      | `tipo_de_comprobante`         | 1 = Factura, 2 = Boleta, 3 = Nota de Crédito, 4 = Nota de Débito.  |
| `sale_document.series`                    | `serie`                       | Debe empezar con 'F' (Facturas) o 'B' (Boletas).                   |
| `sale_document.number`                    | `numero`                      | Autoincremental correlativo por serie (sin ceros a la izquierda).  |
| `customer.document_type`                  | `cliente_tipo_de_documento`   | Mapeo de Enums (6=RUC, 1=DNI, -=VARIOS).                           |
| `customer.document_number`                | `cliente_numero_de_documento` | Número de documento de identidad del cliente.                      |
| `customer.name`                           | `cliente_denominacion`        | Razón social o nombres completos.                                  |
| `sale.created_at`                         | `fecha_de_emision`            | Formato estricto `DD-MM-YYYY`. Debe ser la fecha actual.           |
| `sale.subtotal`                           | `total_gravada`               | Sumatoria del valor de venta de los ítems afectos al impuesto.     |
| `sale.tax`                                | `total_igv`                   | Sumatoria del impuesto calculado de las líneas gravadas.           |
| `sale.total`                              | `total`                       | Monto total a pagar por el comprobante.                            |

### 2. Ítems o Líneas del Detalle

Cada elemento en `sale_item` se itera dentro del arreglo `"items"` del JSON:

| Campo Base de Datos (`sale_item`) | Campo JSON Nubefact | Regla de Transformación / Observaciones                                           |
| :-------------------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| En base a variante / producto     | `unidad_de_medida`  | `NIU` para bienes tangibles, `ZZ` para servicios prestados.                       |
| `sale_item.id` o SKU              | `codigo`            | Identificador interno del producto en el catálogo.                                |
| Detalle de variante               | `descripcion`       | Texto descriptivo claro del producto/servicio comercializado.                     |
| `sale_item.quantity`              | `cantidad`          | Cantidad física vendida (Debe pasar validación `ck_sale_item_quantity_positive`). |
| `sale_item.unit_price` / 1.18     | `valor_unitario`    | Precio unitario neto de impuestos (Sin IGV).                                      |
| `sale_item.unit_price`            | `precio_unitario`   | Precio unitario final al consumidor (Con IGV incluido).                           |
| `sale_item.discount`              | `descuento`         | Descuento aplicado directamente a la línea antes de impuestos.                    |
| `sale_item.subtotal`              | `subtotal`          | `(valor_unitario * cantidad) - descuento`.                                        |
| `sale_item.subtotal` \* 0.18      | `igv`               | Monto del impuesto correspondiente a este ítem.                                   |
| `sale_item.subtotal` + `igv`      | `total`             | Monto total de la línea del detalle.                                              |
| Constante interna                 | `tipo_de_igv`       | Por defecto `1` (Gravado - Operación Onerosa).                                    |

### 3. Flujo Especial: Venta al Crédito

Si el pago (`payment.method`) está definido como crédito, se debe omitir el campo `cancelado: true` en la cabecera y rellenar el arreglo dinámico `"venta_al_credito"`, calculando las cuotas, fechas de vencimiento y montos basándose en los términos de pago acordados.
