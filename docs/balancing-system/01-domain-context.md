# Modelo de Dominio — Balance V1

## Galería Chocca

> **Objetivo:** Definir el modelo de dominio inicial para controlar Activos Corrientes, Pasivos Corrientes y Capital de Trabajo mediante la creación de fotografías financieras históricas (**Snapshots**), tomando como referencia el balance operativo que actualmente gestiona el gerente en Excel.

---

## 1. Objetivo del módulo

El módulo de **Balance** permitirá representar, congelar y controlar la posición financiera de corto plazo de la empresa mediante vistas consolidadas e históricas de:

- **Activos Corrientes**
- **Pasivos Corrientes**
- **Capital de Trabajo**

La posición financiera de la empresa se organiza en fotografías temporales congeladas (**`BalanceSnapshot`**). La fórmula fundamental de V1 será:

$$\text{Capital de Trabajo} = \text{Total Activos Corrientes} - \text{Total Pasivos Corrientes}$$

El módulo no pretende reemplazar el sistema operativo de inventario ni convertirse inicialmente en un sistema contable completo. Su responsabilidad será consolidar, valorizar y congelar la información financiera relevante para la gestión gerencial en momentos determinados del tiempo.

---

## 2. Principio arquitectónico de V1

### 2.1 Fotografía financiera congelada (`BalanceSnapshot`)

El negocio requiere consultar balances de períodos pasados sin temor a que modificaciones operativas o financieras posteriores en el sistema alteren la información registrada. Cada registro financiero en V1 pertenece obligatoriamente a un **Snapshot** que define el marco temporal de la información (`period_start` y `period_end`).

### 2.2 El balance y el inventario son dominios independientes

El sistema ya posee información operativa de inventario mediante entidades como:

- `materials`
- `inventory`
- `inventory_location`
- `inventory_movement`
- Productos y sus variantes

En V1 no se obliga al balance a depender de estas entidades operativas. Dado que el inventario operativo está en proceso de adopción, V1 permite registrar valorizaciones financieras agregadas dentro de un snapshot, evitando crear datos operativos artificiales únicamente para satisfacer una necesidad financiera.

### Evolución prevista

**Fase V1 (Snapshot Financiero Asociado):**

```text
BalanceSnapshot (period_start, period_end)
   │
   ├── accounts_receivable
   ├── inventory_valuations
   ├── accounts_payable
   ├── financial_debts
   └── other_current_liabilities
```

**Fase Futura (Integración Progresiva):**

```text
Inventario operativo
        │
        ↓
Motor de valorización
        │
        ↓
Valorización financiera → BalanceSnapshot
```

_La duplicación temporal de información es deliberada y aceptable mientras ambos dominios maduran._

---

## 3. Lenguaje de dominio

### 3.1 Activos Corrientes

Son recursos que representan valor económico disponible o realizable en el corto plazo. En V1 se consideran:

#### A. Cuentas por cobrar (`accounts_receivable`)

Dinero pendiente de cobro proveniente de clientes, tiendas, consignaciones u otras entidades comerciales para el período evaluado.

_Ejemplos observados en el Excel:_

- Huaraz
- Tienda El Zapatón
- Galería Azul
- Clientes individuales asociados a tiendas/vendedores

#### B. Inventario valorizado (`inventory_valuations`)

Valor económico de existencias físicas o producción en proceso reportado dentro del snapshot. Se divide en:

1. **Materia Prima (`RAW_MATERIAL`):** Materiales e insumos no convertidos en producto terminado (Tela, Camisería, Tocuyo, Metales, Correas, Bolsas, Hangtags, otros avíos).
2. **Trabajo en Proceso (`WORK_IN_PROGRESS`):** Productos o lotes en proceso productivo (Corte/Codificado, Confección, Lavandería).
3. **Producto Terminado (`FINISHED_GOODS`):** Prendas listas para venta situadas en almacén, tiendas o en poder de vendedores/distribuidores.

---

## 4. Pasivos Corrientes

Obligaciones cuyo pago corresponde al corto plazo. En V1 se estructuran en:

#### A. Cuentas por pagar (`accounts_payable`)

Obligaciones comerciales u operativas pendientes con terceros:

- **Proveedores de insumos:** Colortex, Comercial Textil, Texcorp, etc. (pueden asociarse a marcas como _Old Denim_ o _Creator_).
- **Servicios y talleres:** Talleres de confección, lavanderías, servicios externos, maquiladores.

#### B. Deuda financiera (`financial_debts`)

Obligaciones financieras con entidades bancarias o financieras (_BCP_, _BBVA_, _Caja Huancayo_). Se mantienen separadas por su distinta naturaleza económica y su contexto temporal queda totalmente determinado por el `BalanceSnapshot` al que pertenecen.

#### C. Otras obligaciones corrientes (`other_current_liabilities`)

Obligaciones sociales, fiscales y laborales pendientes:

- ESSALUD
- AFP
- Impuestos (SUNAT, IGV, Renta)
- Planillas y cargas sociales pendientes

---

## 5. Entidades principales de V1

Todas las entidades financieras secundarias pertenecen formalmente a un `BalanceSnapshot` mediante su correspondiente atributo conceptual `snapshot_id`.

### 5.1 `balance_snapshots`

Representa una fotografía financiera congelada de la empresa para un período determinado.

- **Campos conceptuales:** `id`, `period_start`, `period_end`, `description`, `status`, `created_at`
- **`period_start` / `period_end`:** Definen el rango de fechas al que corresponde el snapshot.
- **Regla conceptual de integridad:**
  $$\text{period\_start} \le \text{period\_end}$$
- **Propósito:** Garantizar que los balances históricos se conserven intactos ante cualquier cambio operativo o ajuste en períodos futuros.

### 5.2 `accounts_receivable`

Representa dinero pendiente de cobro dentro de un snapshot.

- **Campos conceptuales:** `id`, `snapshot_id`, `brand`, `entity_name`, `location`, `amount`, `status`, `created_at`
- **`brand`:** Identifica la marca (_OLD_DENIM_, _CREATOR_). Se mantiene como texto en V1.
- **`entity_name`:** Cliente, tienda, vendedor o entidad deudora.
- **`location`:** Ubicación o contexto comercial asociado.
- **`amount`:** Monto pendiente.

### 5.3 `accounts_payable`

Representa obligaciones comerciales y operativas pendientes dentro de un snapshot.

- **Campos conceptuales:** `id`, `snapshot_id`, `brand`, `entity_name`, `cost_center`, `amount`, `status`, `created_at`
- **`brand`:** Texto indicativo de la marca.
- **`entity_name`:** Proveedor, taller, lavandería o acreedor.
- **`cost_center`:** Centro de costo operacional (`FABRIC`, `LAUNDRY`, `SEWING`).
- **`amount`:** Monto pendiente de pago.

### 5.4 `financial_debts`

Representa obligaciones con entidades financieras dentro de un snapshot.

- **Campos conceptuales:** `id`, `snapshot_id`, `bank_name`, `amount`, `status`, `created_at`
- **`bank_name`:** Nombre del banco o entidad financiera (_BCP_, _BBVA_, _CAJA_HUANCAYO_).
- **`amount`:** Monto de la deuda acumulada a la fecha del snapshot.
- _Decisión de diseño:_ Se elimina `fiscal_year` como atributo directo; el marco temporal viene dado directamente por el `BalanceSnapshot` contenedor.

### 5.5 `other_current_liabilities`

Representa obligaciones fiscales, sociales y laborales dentro de un snapshot.

- **Campos conceptuales:** `id`, `snapshot_id`, `category`, `entity_name`, `description`, `amount`, `status`, `created_at`
- **`category`:** Clasificación conceptual (`TAXES`, `ESSALUD`, `AFP`, `PAYROLL`, `OTHER`).
- **`entity_name` / `description`:** Detalle o entidad acreedora (ej. "SUNAT - IGV Agosto", "AFP Integra").
- **`amount`:** Monto adeudado.

### 5.6 `inventory_valuations`

Representa la valorización financiera agregada del inventario para el snapshot (no el inventario operativo).

- **Campos conceptuales:** `id`, `snapshot_id`, `category`, `subcategory`, `description`, `brand`, `location`, `quantity`, `unit_value`, `created_at`
- **Fórmula de cálculo:**
  $$\text{total\_value} = \text{quantity} \times \text{unit\_value}$$

---

## 6. Categorías de `inventory_valuations`

| Categoría              | Subcategorías / Ubicaciones    | Ejemplos / Alcance                                          |
| :--------------------- | :----------------------------- | :---------------------------------------------------------- |
| **`RAW_MATERIAL`**     | —                              | TELA, CAMISERIA, TOCUYO, METALES, CORREAS, BOLSAS, HANGTAGS |
| **`WORK_IN_PROGRESS`** | `CUTTING`, `SEWING`, `LAUNDRY` | Corte/Codificado, Confección, Lavandería                    |
| **`FINISHED_GOODS`**   | `WAREHOUSE`, `STORE`, `SELLER` | Prendas terminadas en stock o distribución                  |

---

## 7. Regla de integridad en la Valorización

El cálculo de la valorización responde al principio:
$$\text{total\_value} = \text{quantity} \times \text{unit\_value}$$

> **Regla:** `total_value` debe ser siempre una propiedad derivada o un valor calculado dinámicamente. El usuario ingresa `quantity` y `unit_value`. Esto evita inconsistencias en el snapshot (ejemplo: si `quantity = 100` y `unit_value = 20`, el resultado debe ser rigurosamente `2000`).

---

## 8. Marco temporal y Snapshots

En V1 el parámetro temporal se delimita formalmente en `balance_snapshots`:

- **`period_start`**: Fecha inicial del período del snapshot.
- **`period_end`**: Fecha final del período del snapshot.
- **Invariante:** $\text{period\_start} \le \text{period\_end}$.

Esto permite comparar snapshots de distintos rangos (ejemplo: Snapshot Quincenal, Mensual de Agosto vs. Septiembre) y analizar la evolución real del Capital de Trabajo.

---

## 9. Marcas

Mantenidas como campo de texto libre en V1 (`OLD DENIM`, `CREATOR`) dentro de cuentas por pagar, cuentas por cobrar y valorizaciones de inventario. No se crea una entidad maestra de marcas obligatoria para no acoplar dominios prematuramente.

---

## 10. Ubicaciones

Mantenidas como texto en V1 (`ALMACEN`, `TIENDA`, `EDWIN`, `CARLOS`, `CINTYA`, `YERITZON`, `CONFECCION`, `LAVANDERIA`, `CORTE/CODIFICADO`). En versiones futuras se podrá vincular mediante clave foránea a `inventory_location.id`.

---

## 11. Estados (`status`)

Conjuntos de enums controlados por entidad:

- **Snapshot (`balance_snapshots`):** `DRAFT`, `CLOSED`, `ARCHIVED`
- **Cuentas por pagar (`accounts_payable`):** `PENDING`, `PARTIALLY_PAID`, `PAID`, `CANCELLED`
- **Cuentas por cobrar (`accounts_receivable`):** `PENDING`, `PARTIALLY_COLLECTED`, `COLLECTED`, `CANCELLED`
- **Deuda financiera (`financial_debts`):** `ACTIVE`, `PARTIALLY_PAID`, `PAID`, `CANCELLED`
- **Otras obligaciones (`other_current_liabilities`):** `PENDING`, `PARTIALLY_PAID`, `PAID`, `CANCELLED`

---

## 12. Centros de Costo (`cost_center`)

Clasificación operacional libre en cuentas por pagar: `FABRIC`, `SEWING`, `LAUNDRY`, ampliable en el tiempo.

---

## 13. Estructura conceptual del Balance

```text
                     BALANCE SNAPSHOT
           (period_start <= period_end)
                        │
         ┌──────────────┴──────────────┐
         │                             │
   ACTIVOS CORRIENTES          PASIVOS CORRIENTES
         │                             │
   ┌─────┴─────┐              ┌────────┼─────────┐
   │           │              │        │         │
Receivables   Inventory     Payables Financial Other Current
             Valuations              Debts    Liabilities
                  │                            (Taxes, ESSALUD,
         ┌────────┼────────┐                    AFP, Payroll)
         │        │        │
     Raw Material WIP   Finished Goods
                  │
           ┌──────┼──────┐
           │      │      │
         Cutting Sewing Laundry
```

---

## 14. Cálculo del Balance

Las operaciones de consolidación sobre un snapshot se definen de la siguiente manera:

### Activos Corrientes

$$\text{Total Activos Corrientes} = \text{Total Receivables} + \text{Total Raw Material} + \text{Total WIP} + \text{Total Finished Goods}$$

### Pasivos Corrientes

$$\text{Total Pasivos Corrientes} = \text{Total Payables} + \text{Total Financial Debts} + \text{Total Other Current Liabilities}$$

### Capital de Trabajo

$$\text{Capital de Trabajo} = \text{Total Activos Corrientes} - \text{Total Pasivos Corrientes}$$

---

## 15. Arquitectura de Cálculo y Responsabilidad del `BalanceCalculator`

### 15.1 Componente Puro de Cálculo

El `BalanceCalculator` es un componente de lógica pura en memoria:

- **NO consulta repositorios ni base de datos.**
- **NO realiza operaciones de I/O ni conoce detalles de la persistencia.**
- Recibe un objeto de contexto con los datos del snapshot previamente cargados (`BalanceCalculationContext`).
- Aplica las reglas aritméticas y devuelve un resultado inmutable (`BalanceResult`).

### 15.2 Flujo de Ejecución Conceptual

```text
Repository / Service
        │
        ├─► (Carga snapshot y entidades secundarias desde DB)
        │
        ▼
BalanceCalculationContext
        │
        ├─► (Estructura datos en memoria)
        │
        ▼
BalanceCalculator
        │
        ├─► (Aplica fórmulas de activos, pasivos y capital de trabajo)
        │
        ▼
BalanceResult
```

### 15.3 Representación Conceptual del Flujo

```python
# 1. El repositorio o servicio consulta la DB y arma el contexto
context = BalanceCalculationContext(
    snapshot_id=snapshot.id,
    period_start=snapshot.period_start,
    period_end=snapshot.period_end,
    receivables=accounts_receivable_list,
    valuations=inventory_valuations_list,
    payables=accounts_payable_list,
    financial_debts=financial_debts_list,
    other_liabilities=other_current_liabilities_list,
)

# 2. El Calculator procesa de forma pura el contexto recibido
result: BalanceResult = BalanceCalculator.calculate(context)
```

---

## 16. Relación con el inventario operativo

En V1, las tablas operativas (`materials`, `inventory`, `inventory_location`, `inventory_movement`) **no** poseen claves foráneas hacia `inventory_valuations`. La valorización financiera se ingresa o consolida a nivel de snapshot de forma independiente para evitar acoplar procesos inmaduros.

---

## 17. Evolución futura

Cuando el dominio de inventario operativo alcance suficiente madurez:

```text
Material → Inventory → Inventory Movement → Stock Actual → Costo/Precio → Inventory Valuation → BalanceSnapshot
```

En ese momento se podrán introducir campos opcionales como `material_id`, `product_id` o `inventory_location_id` en `inventory_valuations`.

---

## 18. Lo que NO intenta resolver V1

V1 se limita a digitalizar y congelar la fotografía financiera gerencial de corto plazo. **No pretende ser:**

- Un sistema contable completo / libro mayor / sistema de partida doble.
- Un sistema de facturación o tributario automático.
- Un motor de depreciación de activos fijos.
- Un módulo de costos de producción detallado paso a paso.

---

## 19. Principio fundamental del diseño

> **El balance representa el valor financiero congelado del negocio en un snapshot (`period_start` a `period_end`); el inventario representa la realidad operativa del stock en tiempo real.**

Flujo evolutivo:

```text
[V1] Registro de Snapshot Manual ─────────────────► BalanceCalculationContext ──► BalanceCalculator ──► BalanceResult
[V2] Inventario Operativo ──► Motor Valorización ──► BalanceSnapshot ───────────► BalanceCalculator ──► BalanceResult
```

---

## 20. Modelo V1 Resumido

```text
BALANCE V1
│
└── balance_snapshots (id, period_start, period_end, status)
    │   (Regla de integridad: period_start <= period_end)
    │
    ├── ACTIVOS CORRIENTES
    │   ├── accounts_receivable
    │   └── inventory_valuations
    │       ├── RAW_MATERIAL
    │       ├── WORK_IN_PROGRESS (CUTTING, SEWING, LAUNDRY)
    │       └── FINISHED_GOODS
    │
    └── PASIVOS CORRIENTES
        ├── accounts_payable (Suppliers, Workshops, Services)
        ├── financial_debts
        └── other_current_liabilities (Taxes, ESSALUD, AFP, Payroll)
```

$$\text{CURRENT ASSETS} - \text{CURRENT LIABILITIES} = \text{WORKING CAPITAL}$$

---

_Este documento constituye la especificación conceptual cerrada del **Modelo de Dominio — Balance V1** de Galería Chocca y servirá como referencia para la implementación de modelos SQLModel, repositorios, servicios y DTOs._
