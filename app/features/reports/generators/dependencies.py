from app.features.reports.generators.inventory_movement_report import InventoryMovementExcelReportGenerator

def get_inventory_movement_excel_report_generator(
) -> InventoryMovementExcelReportGenerator:

    return InventoryMovementExcelReportGenerator()