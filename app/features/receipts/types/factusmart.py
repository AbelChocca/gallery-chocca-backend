from dataclasses import dataclass
from decimal import Decimal


@dataclass
class FactuSmartCustomerDTO:
    codigo_tipo_documento_identidad: str
    numero_documento: str


@dataclass
class FactuSmartItemDTO:
    codigo_interno: str
    descripcion: str
    unidad_de_medida: str
    cantidad: Decimal

    valor_unitario: Decimal
    codigo_tipo_precio: str
    precio_unitario: Decimal

    codigo_tipo_afectacion_igv: str
    total_base_igv: Decimal
    porcentaje_igv: Decimal
    total_igv: Decimal
    total_impuestos: Decimal

    total_valor_item: Decimal
    total_item: Decimal


@dataclass
class FactuSmartTotalsDTO:
    total_operaciones_gravadas: Decimal
    total_igv: Decimal
    total_impuestos: Decimal
    total_valor: Decimal
    total_venta: Decimal


@dataclass
class FactuSmartSunatDTO:
    codigo: str | None = None
    descripcion: str | None = None


@dataclass
class FactuSmartIssueResponseDTO:
    success: bool

    estado: str
    estado_descripcion: str

    serie_numero: str
    external_id: str

    aceptado_por_sunat: bool

    sunat: FactuSmartSunatDTO | None

    entorno: str | None
    tiene_validez_fiscal: bool

    creditos_restantes: int | None