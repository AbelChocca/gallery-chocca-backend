# Balancing V1 — Frontend UX/UI Guide

## Galería Chocca

> **Objetivo:** Diseñar una experiencia de gestión financiera simple, visual y empresarial para que el gerente pueda entender y controlar la posición financiera de Galería Chocca sin necesidad de conocimientos contables avanzados.

---

# 1. Principio de producto

El sistema debe sentirse como un **panel de control del negocio**, no como un software contable.

El usuario principal es el gerente.

La interfaz debe responder rápidamente:

1. ¿Cómo está la empresa?
2. ¿Cuánto dinero tenemos pendiente de cobrar?
3. ¿Cuánto debemos?
4. ¿Cuánto dinero tenemos invertido en inventario?
5. ¿Cuánto capital de trabajo tenemos?
6. ¿Estamos mejor o peor que el período anterior?
7. ¿Dónde está concentrado nuestro dinero?

### Regla principal

> **El gerente debe poder entender el estado financiero principal de la empresa en menos de 30 segundos.**

---

# 2. Filosofía UX

## 2.1 Simpleza sobre densidad

No mostrar demasiada información al mismo tiempo.

Evitar:

- tablas gigantes
- terminología contable innecesaria
- formularios complejos
- múltiples filtros visibles simultáneamente
- números sin contexto
- dashboards saturados

Preferir:

- Cards
- Resúmenes
- Estados
- Comparaciones
- Breakdown progresivo
- Acciones contextuales
- tablas simples cuando sean necesarias

---

# 3. Modelo mental del usuario

El gerente debe percibir el sistema como:

```text
                    BALANCE
                       │
              "¿Cómo estamos?"
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Tenemos         Debemos       Tenemos
     pendiente       pendiente     invertido
        │              │              │
        ↓              ↓              ↓
    Por cobrar      Por pagar     Inventario
                       │
                       ↓
                Capital de trabajo
```

No debe necesitar comprender:

```text
Assets
Liabilities
Accounting entries
General ledger
Double-entry accounting
```

La terminología financiera puede aparecer, pero siempre acompañada de lenguaje humano.

---

# 4. Arquitectura de navegación

```text
Galería Chocca
│
├── Dashboard
│
├── Ventas
│
├── Inventario
│
├── Pricing
│
└── Balance
    │
    ├── Resumen
    ├── Cuentas por cobrar
    ├── Cuentas por pagar
    ├── Deudas financieras
    ├── Otras obligaciones
    ├── Inventario valorizado
    └── Historial
```

El módulo de Balance debe sentirse como una sección más del ERP, no como una aplicación independiente.

---

# 5. Página principal — Balance

Ruta conceptual:

```text
/balancing
```

Esta es la pantalla más importante del módulo.

## Estructura

```text
┌─────────────────────────────────────────────────────────────┐
│ Balance                                  Agosto 2026   ▼     │
│ Última actualización: 27 Ago 2026                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Capital de Trabajo                                          │
│ S/ 88,000                              ↑ S/ 7,000 vs Julio  │
│                                                             │
├───────────────────┬───────────────────┬─────────────────────┤
│ Activos Corrientes│ Pasivos Corrientes│ Inventario          │
│ S/ 185,000        │ S/ 97,000         │ S/ 125,000         │
│ ↑ 7.5%            │ ↑ 6.6%            │ ↑ 4.2%             │
└───────────────────┴───────────────────┴─────────────────────┘

┌──────────────────────────────┐
│ Dinero por cobrar            │
│ S/ 42,000                    │
│                              │
│ 35k pendientes               │
│ 7k parcialmente cobrados     │
│                              │
│ Ver cuentas →                │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Dinero por pagar             │
│ S/ 51,000                    │
│                              │
│ 42k pendientes               │
│ 9k parcialmente pagados      │
│                              │
│ Ver cuentas →                │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Inventario                   │
│                              │
│ Materia prima      45k       │
│ En producción      30k       │
│ Producto terminado 50k      │
│                              │
│ Ver inventario →             │
└──────────────────────────────┘
```

---

# 6. Balance Header

Crear componente:

```text
BalanceHeader
```

Responsabilidades:

- título
- período actual
- fecha de actualización
- selector de snapshot
- acción "Crear snapshot"

Ejemplo:

```text
Balance

Agosto 2026                    [Cambiar período ▼]

Última actualización
27 Ago 2026 · 10:32 AM
```

---

# 7. Working Capital Card

Crear:

```text
WorkingCapitalCard
```

Debe ser el elemento visual principal.

Mostrar:

```text
Capital de trabajo

S/ 88,000

↑ S/ 7,000
vs período anterior
```

Nunca mostrar solamente:

```text
Working Capital: 88000
```

Siempre mostrar:

- valor
- variación
- período de comparación
- contexto

---

# 8. Financial Overview

Crear:

```text
FinancialOverview
```

Contiene:

```text
CurrentAssetsCard
CurrentLiabilitiesCard
WorkingCapitalCard
```

Layout:

```text
┌──────────────┐
│ Activos      │
│ S/185,000    │
└──────────────┘

┌──────────────┐
│ Pasivos      │
│ S/97,000     │
└──────────────┘

┌──────────────┐
│ Capital      │
│ S/88,000     │
└──────────────┘
```

---

# 9. Financial Breakdown

Crear:

```text
FinancialBreakdown
```

Mostrar:

### Activos

```text
Cuentas por cobrar       S/ 42,000
Inventario               S/125,000
───────────────────────────────────
Total                    S/167,000
```

### Pasivos

```text
Cuentas por pagar        S/51,000
Deudas financieras       S/30,000
Otras obligaciones       S/16,000
───────────────────────────────────
Total                    S/97,000
```

El usuario debe poder hacer click sobre cada línea.

---

# 10. Accounts Receivable

Ruta:

```text
/balancing/accounts-receivable
```

Crear:

```text
AccountsReceivablePage
```

Componentes:

```text
AccountsReceivableHeader
AccountsReceivableSummary
AccountsReceivableFilters
AccountsReceivableTable
AccountsReceivableForm
```

---

# 11. Accounts Receivable Summary

Mostrar tres o cuatro métricas:

```text
Total por cobrar       S/42,000
Pendiente              S/35,000
Parcialmente cobrado   S/7,000
Cobrado                S/15,000
```

No convertir estas métricas en gráficos innecesarios.

---

# 12. Accounts Receivable Table

Columnas:

```text
Cliente
Marca
Ubicación
Monto
Estado
Acciones
```

Ejemplo:

```text
Huaraz
OLD DENIM
Huaraz
S/ 8,500
Pendiente
...

Tienda El Zapatón
CREATOR
Lima
S/ 4,200
Parcial
...
```

Acciones:

```text
Ver
Editar
Eliminar
```

---

# 13. Accounts Payable

Ruta:

```text
/balancing/accounts-payable
```

Componentes:

```text
AccountsPayablePage
AccountsPayableSummary
AccountsPayableFilters
AccountsPayableTable
AccountsPayableForm
```

Tabla:

```text
Acreedor
Marca
Centro de costo
Monto
Estado
Acciones
```

Filtros:

```text
Estado
Marca
Centro de costo
```

---

# 14. Financial Debts

Ruta:

```text
/balancing/financial-debts
```

Componentes:

```text
FinancialDebtPage
FinancialDebtSummary
FinancialDebtFilters
FinancialDebtTable
FinancialDebtForm
```

Tabla:

```text
Banco
Monto
Estado
Año
Acciones
```

El banco debe mostrarse como nombre legible.

Ejemplo:

```text
BCP
BBVA
Caja Huancayo
```

---

# 15. Other Current Liabilities

Ruta:

```text
/balancing/other-current-liabilities
```

Componentes:

```text
OtherCurrentLiabilitiesPage
OtherCurrentLiabilitiesSummary
OtherCurrentLiabilitiesFilters
OtherCurrentLiabilitiesTable
OtherCurrentLiabilityForm
```

Ejemplos:

```text
ESSALUD
AFP
Impuestos
Planillas
```

---

# 16. Inventory Valuation

Ruta:

```text
/balancing/inventory-valuations
```

Componentes:

```text
InventoryValuationPage
InventoryValuationSummary
InventoryValuationBreakdown
InventoryValuationFilters
InventoryValuationTable
InventoryValuationForm
```

---

# 17. Inventory Breakdown

Mostrar primero:

```text
Inventario total

S/ 125,000
```

Después:

```text
Materia Prima
S/45,000

En producción
S/30,000

Producto Terminado
S/50,000
```

Y al entrar:

```text
Materia Prima
├── Tela
├── Camisería
├── Tocuyo
├── Metales
├── Correas
└── Otros

Trabajo en proceso
├── Corte
├── Confección
└── Lavandería

Producto terminado
├── Almacén
├── Tiendas
└── Vendedores
```

---

# 18. Inventory Valuation Form

El formulario debe sentirse extremadamente simple.

```text
Nueva valorización

Categoría
[ Materia Prima ▼ ]

Subcategoría
[ Tela ▼ ]

Descripción
[ Tela Denim 12oz ]

Marca
[ Old Denim ▼ ]

Ubicación
[ Almacén ▼ ]

Cantidad
[ 500 ]

Valor unitario
[ S/ 20.00 ]

──────────────────────

Valor total
S/ 10,000

              [Cancelar] [Guardar]
```

`total_value` nunca debe ser editable.

Debe actualizarse automáticamente:

```text
Cantidad × Valor unitario
```

---

# 19. Snapshot Management

Ruta:

```text
/balancing/snapshots
```

Crear:

```text
SnapshotHistoryPage
SnapshotList
SnapshotCard
SnapshotForm
```

La pantalla debe parecer un historial de períodos:

```text
Balance

┌─────────────────────────────────────────┐
│ Agosto 2026                             │
│ 01 Ago — 31 Ago                         │
│ Capital de trabajo: S/88,000            │
│                                         │
│ [Ver balance]                           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Julio 2026                              │
│ 01 Jul — 31 Jul                         │
│ Capital de trabajo: S/81,000            │
│                                         │
│ [Ver balance]                           │
└─────────────────────────────────────────┘
```

---

# 20. Create Snapshot

El formulario debe tener únicamente:

```text
Nuevo período

Fecha inicial
[ 01/08/2026 ]

Fecha final
[ 31/08/2026 ]

                [Crear snapshot]
```

No pedir datos financieros durante la creación.

Los datos financieros pertenecen al snapshot y se agregan posteriormente.

---

# 21. Snapshot Selector

Crear:

```text
SnapshotSelector
```

Debe ser reutilizable en todo el módulo.

Ejemplo:

```text
Período

[ Agosto 2026 ▼ ]
```

Opciones:

```text
Agosto 2026
Julio 2026
Junio 2026
Mayo 2026
```

---

# 22. Comparison

Ruta:

```text
/balancing/comparison
```

Crear:

```text
BalanceComparisonPage
ComparisonSelector
ComparisonSummary
ComparisonMetric
```

Selector:

```text
Comparar

[ Agosto 2026 ▼ ]

vs

[ Julio 2026 ▼ ]
```

Resultado:

```text
Activos corrientes

Julio
S/172,000

Agosto
S/185,000

↑ S/13,000
```

---

# 23. Comparison Summary

Mostrar:

```text
Activos
S/185,000
↑ S/13,000

Pasivos
S/97,000
↑ S/6,000

Capital de trabajo
S/88,000
↑ S/7,000
```

La variación debe utilizar lenguaje visual:

```text
↑ aumentó
↓ disminuyó
— sin cambios
```

No depender únicamente del color.

---

# 24. Forms UX

Todos los formularios CRUD deben seguir el mismo patrón.

```text
Form
│
├── Header
│
├── Main fields
│
├── Financial fields
│
├── Derived values
│
└── Actions
```

Ejemplo:

```text
Nueva cuenta por cobrar

Cliente
[________________]

Marca
[ OLD DENIM ▼ ]

Ubicación
[________________]

Monto
[ S/ __________ ]

Estado
[ Pendiente ▼ ]

              [Cancelar] [Guardar]
```

---

# 25. Empty States

Nunca mostrar una tabla vacía sin explicación.

Ejemplo:

```text
No hay cuentas por cobrar

Todavía no has registrado cuentas por cobrar
para este período.

[Agregar cuenta]
```

Para inventario:

```text
No hay valorizaciones

Agrega la primera valorización de inventario
para comenzar a controlar este período.

[Agregar valorización]
```

---

# 26. Loading States

Usar skeletons para:

- cards
- tablas
- métricas
- snapshots

Evitar loaders gigantes que bloqueen toda la pantalla.

---

# 27. Error States

Los errores deben ser humanos.

Evitar:

```text
500 INTERNAL SERVER ERROR
```

Preferir:

```text
No pudimos cargar el balance

Intenta nuevamente.

[Reintentar]
```

---

# 28. Confirmation Dialogs

Eliminar una entidad debe requerir confirmación.

Ejemplo:

```text
¿Eliminar esta cuenta?

Esta acción no se puede deshacer.

[Cancelar] [Eliminar]
```

Para acciones financieras importantes, mostrar claramente qué registro será eliminado.

---

# 29. Componentes reutilizables

Crear componentes genéricos que puedan utilizarse en todo Balancing:

```text
BalanceCard
FinancialMetricCard
FinancialStatusBadge
SnapshotSelector
PeriodSelector
FinancialTable
FinancialFilters
FinancialForm
AmountInput
FinancialSummary
EmptyState
ErrorState
ConfirmDialog
```

---

# 30. Componentes específicos

```text
WorkingCapitalCard

AccountsReceivableSummary
AccountsPayableSummary
FinancialDebtSummary
OtherCurrentLiabilitiesSummary
InventoryValuationSummary

InventoryBreakdown

BalanceComparison
SnapshotHistory
```

---

# 31. Design System

El módulo debe utilizar los componentes existentes del ERP.

No crear un segundo design system.

Reutilizar:

- Buttons
- Inputs
- Selects
- Dialogs
- Dropdowns
- Cards
- Tables
- Badges
- Tooltips
- Skeletons

El Balance debe sentirse parte del mismo producto.

---

# 32. Responsive Design

Desktop-first porque el usuario principal es el gerente.

Sin embargo:

```text
Desktop
Tablet
Mobile
```

deben funcionar correctamente.

En mobile:

```text
3 cards
```

pueden convertirse en:

```text
1 card
1 card
1 card
```

Las tablas pueden convertirse en cards cuando sea necesario.

---

# 33. UX de números financieros

Todos los montos deben utilizar formato consistente:

```text
S/ 125,000.00
```

Nunca:

```text
125000
```

Nunca mezclar:

```text
S/.125,000
S/125000
125k
```

en la misma pantalla.

Para métricas grandes se puede utilizar:

```text
S/ 125k
```

únicamente cuando el contexto lo permita.

---

# 34. Estados financieros

Utilizar badges consistentes:

```text
PENDING
PARTIALLY_PAID
PAID
CANCELLED
```

Mostrar al usuario:

```text
Pendiente
Pago parcial
Pagado
Cancelado
```

Nunca mostrar los enums técnicos directamente.

---

# 35. Progressive Disclosure

La interfaz principal debe mostrar:

```text
Resumen
```

El usuario puede profundizar:

```text
Resumen
   ↓
Categoría
   ↓
Detalle
   ↓
Registro
```

No mostrar todo desde el principio.

---

# 36. Dashboard Mental Model

La experiencia completa debería sentirse así:

```text
ENTRO
  ↓
"¿Cómo estamos?"
  ↓
Capital de trabajo
  ↓
"¿Por qué?"
  ↓
Activos / Pasivos
  ↓
"¿Dónde está el dinero?"
  ↓
CxC / Inventario
  ↓
"¿Qué debemos?"
  ↓
CxP / Deudas / Obligaciones
  ↓
"¿Estamos mejor que antes?"
  ↓
Comparación
```

---

# 37. Reglas de UX más importantes

### Regla 1

> Una pantalla debe tener una acción principal clara.

### Regla 2

> Los números siempre deben tener contexto.

### Regla 3

> No mostrar terminología técnica cuando exista una forma más humana de expresarla.

### Regla 4

> No obligar al usuario a navegar entre muchas pantallas para responder una pregunta simple.

### Regla 5

> Los formularios deben pedir únicamente información necesaria.

### Regla 6

> Las métricas calculadas nunca deben ser editables.

### Regla 7

> El período seleccionado debe permanecer visible.

### Regla 8

> Las tablas sirven para administrar registros; las cards sirven para entender el negocio.

---

# 38. Arquitectura final de componentes

```text
Balancing
│
├── BalanceDashboard
│   ├── BalanceHeader
│   ├── SnapshotSelector
│   ├── WorkingCapitalCard
│   ├── FinancialOverview
│   ├── FinancialBreakdown
│   └── BalanceInsights
│
├── AccountsReceivable
│   ├── Summary
│   ├── Filters
│   ├── Table
│   └── Form
│
├── AccountsPayable
│   ├── Summary
│   ├── Filters
│   ├── Table
│   └── Form
│
├── FinancialDebts
│   ├── Summary
│   ├── Filters
│   ├── Table
│   └── Form
│
├── OtherCurrentLiabilities
│   ├── Summary
│   ├── Filters
│   ├── Table
│   └── Form
│
├── InventoryValuations
│   ├── Summary
│   ├── Breakdown
│   ├── Filters
│   ├── Table
│   └── Form
│
├── Snapshots
│   ├── SnapshotHistory
│   ├── SnapshotCard
│   └── SnapshotForm
│
└── Comparison
    ├── ComparisonSelector
    ├── ComparisonSummary
    └── ComparisonMetric
```

---

# 39. Regla de oro

El frontend de Balancing V1 debe cumplir esta sensación:

> **"No sé de contabilidad, pero sé exactamente cómo está mi negocio."**

El gerente no debería pensar:

> "¿Qué significa este asiento?"

Debería pensar:

> "Tenemos S/88,000 de capital de trabajo. Tenemos S/42,000 por cobrar, S/97,000 de obligaciones y S/125,000 invertidos en inventario."

Ese es el objetivo del diseño.

---

# 40. Criterio de éxito

Balancing V1 estará correctamente diseñado si un gerente puede:

- Ver el estado financiero actual en menos de 30 segundos.
- Crear un nuevo período sin asistencia técnica.
- Registrar una cuenta por cobrar rápidamente.
- Registrar una obligación rápidamente.
- Registrar una valorización de inventario sin comprender contabilidad.
- Identificar cuánto dinero está pendiente de cobrar.
- Identificar cuánto dinero debe pagar.
- Entender cuánto capital de trabajo tiene.
- Comparar dos períodos.
- Identificar rápidamente si la situación mejoró o empeoró.

**Si una interacción requiere explicar el sistema al gerente, probablemente la UX todavía puede simplificarse.**
