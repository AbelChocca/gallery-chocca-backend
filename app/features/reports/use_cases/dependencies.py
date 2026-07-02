from app.features.reports.use_cases.generate_inventory_movement_excel_report import GenerateInventoryMovementExcelReportUseCase
from app.features.reports.generators.inventory_movement_report import InventoryMovementExcelReportGenerator
from app.features.reports.builders.inventory_movement_report_builder import InventoryMovementReportBuilder

from app.features.reports.builders.dependency import get_inventory_movement_report_builder
from app.features.reports.generators.dependencies import get_inventory_movement_excel_report_generator

from fastapi import Depends

def get_generate_inventory_movement_excel_report_use_case(
    builder: InventoryMovementReportBuilder = Depends(get_inventory_movement_report_builder),
    generator: InventoryMovementExcelReportGenerator = Depends(get_inventory_movement_excel_report_generator)
) -> GenerateInventoryMovementExcelReportUseCase:

    return GenerateInventoryMovementExcelReportUseCase(
        builder=builder,
        generator=generator
    )