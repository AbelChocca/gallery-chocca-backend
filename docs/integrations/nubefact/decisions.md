# Registro de Decisiones de Arquitectura (ADR)

Este documento detalla las decisiones técnicas y de diseño implementadas para la interoperabilidad entre el sistema ERP local y el proveedor Nubefact.

## 1. Persistencia Previa vs. Generación Directa

- **Decisión:** Toda transacción se guarda obligatoriamente en las tablas `sale` y `sale_item` con estado `PENDING` antes de efectuar la llamada de red a la API de Nubefact.
- **Sustento:** Previene la pérdida de traza comercial local en caso de caídas de conectividad (Timeouts, cortes de internet) y garantiza que los identificadores de venta internos ya existan al poblar el campo `codigo_unico`.

## 2. Manejo de la Serie y Correlatividad

- **Decisión:** La base de datos mantiene un índice único compuesto en `sale_document` para `(document_type, series, number)`. La asignación del correlativo (`number`) se gestiona desde el backend mediante bloqueos optimistas por serie.
- **Sustento:** La SUNAT exige correlatividad estricta sin saltos. Al centralizar y validar la unicidad a nivel de base de datos, se evitan errores concurrentes de duplicidad en entornos de alta demanda.

## 3. Almacenamiento de Enlaces y Documentos

- **Decisión:** No se descargan ni almacenan los archivos binarios (PDF, XML, CDR) de forma nativa en nuestro servidor de base de datos. En su lugar, se guardan las cadenas URL proporcionadas por Nubefact (`enlace_del_pdf`, `enlace_del_xml`, `enlace_del_cdr`) en la tabla `sale_document`.
- **Sustento:** Reduce drásticamente los costos de almacenamiento en disco e infraestructura del ERP, delegando la alta disponibilidad del almacenamiento en la nube de Nubefact. En caso de requerirse almacenamiento local por compliance futuro, se activará el parámetro `pdf_zip_base64` para persistir el binario codificado directamente de la respuesta estructurada.

## 4. Validación Rigurosa de Reglas de Negocio en Tipos de Datos

- **Decisión:** Implementación de `Checks` a nivel de base de datos (`ck_sale_item_quantity_positive`, `ck_sale_item_unit_price_positive`, etc.) alineados con los tipos `Numeric` e `Integer` exigidos por Nubefact.
- **Sustento:** Evita llamadas fallidas innecesarias a la API por inconsistencias de redondeo o datos negativos, optimizando el ancho de banda y la tasa de éxito de la integración.
