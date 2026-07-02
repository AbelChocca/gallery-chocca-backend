from app.features.reports.dto import ColumnDefinition
from app.features.inventory.types import InventoryOwnerType
from zoneinfo import ZoneInfo

LIMA_TZ = ZoneInfo("America/Lima")

MOVEMENTS_COLUMNS = [
    ColumnDefinition("Fecha", 20),
    ColumnDefinition("Codigo", 35), 
    ColumnDefinition("Item", 35),
    ColumnDefinition("Tipo Movimiento", 20),
    ColumnDefinition("Razón", 30),
    ColumnDefinition("Stock Anterior", 15),
    ColumnDefinition("Cantidad", 15),
    ColumnDefinition("Stock Nuevo", 15),
]


SUMMARY_COLUMNS = [
    ColumnDefinition("Item", 35),

    ColumnDefinition("Entradas", 15),
    ColumnDefinition("Ventas", 15),

    ColumnDefinition("Devoluciones Cliente", 22),
    ColumnDefinition("Devoluciones Proveedor", 24),

    ColumnDefinition("Ajuste (+)", 15),
    ColumnDefinition("Ajuste (-)", 15),

    ColumnDefinition("Stock Final", 15),
]


METRICS_COLUMNS = [
    ColumnDefinition("Métrica", 30),
    ColumnDefinition("Valor", 20),
]

REPORT_CONTEXT_NAMES = {
    InventoryOwnerType.MATERIAL: "Materiales",
    InventoryOwnerType.PRODUCT: "Productos",
}