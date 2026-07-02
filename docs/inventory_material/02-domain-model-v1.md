# Domain Model V1 - Inventory Supplies

## Objetivo

Representar las principales entidades identificadas durante la fase inicial de análisis del módulo de inventario de insumos.

## Entidades Identificadas

### Categoria

Responsabilidad:
Clasificar insumos para facilitar su organización y búsqueda.

### Insumo

Responsabilidad:
Representar un material gestionado por la empresa.

### MovimientoInventario

Responsabilidad:
Registrar cambios de stock generados por entradas, salidas o ajustes.

## Diagrama

```mermaid
classDiagram

class Categoria {
    +nombre
    +descripcion
}

class Insumo {
    +codigo
    +nombre
    +descripcion
    +stockActual
    +stockMinimo
    +activo
}

class MovimientoInventario {
    +tipoMovimiento
    +cantidad
    +motivo
    +fechaMovimiento
    +stockResultante
}

class TipoMovimiento {
    <<enumeration>>
    ENTRADA
    SALIDA
    AJUSTE
    DEVOLUCION
    MERMA
}

class EstadoDisponibilidad {
    <<enumeration>>
    DISPONIBLE
    CRITICO
    AGOTADO
}

Categoria "1" --> "*" Insumo : clasifica

Insumo "1" --> "*" MovimientoInventario : registra

MovimientoInventario ..> TipoMovimiento
Insumo ..> EstadoDisponibilidad
```

## Observaciones

- Modelo preliminar sujeto a validación con el contador.
- Las categorías podrían convertirse en catálogo administrable.
- Los movimientos actualmente consideran entradas y salidas.
- Ajustes, mermas y devoluciones requieren validación.

## Próximos pasos

- Validar hipótesis de negocio.
- Confirmar tipos de movimiento.
- Diseñar agregados del dominio.
- Diseñar esquema de base de datos.
