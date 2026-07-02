from datetime import datetime

from app.features.reports.constants import REPORT_CONTEXT_NAMES
from app.features.inventory.inventory_service import InventoryService
from app.features.inventory.inventory_movement_entity import InventoryMovement
from app.features.inventory.dto import InventoryMovementFilters
from app.features.inventory.types import (
    InventoryOwnerType,
    InventoryMovementType
)

from app.features.reports.dto import (
    InventoryMovementReportData,
    InventoryMovementReportRow,
    ReportMetadata,
    InventoryOwnerSummaryRow,
    InventoryReportMetrics
)

class InventoryMovementReportBuilder:

    def __init__(
        self,
        inventory_service: InventoryService
    ) -> None:

        self._inventory_service = (
            inventory_service
        )

    async def build(
        self,
        *,
        owner_type: InventoryOwnerType,
        start_date: datetime,
        end_date: datetime
    ) -> InventoryMovementReportData:

        movements = await (
            self._inventory_service
            .get_inventory_movements(
                filter_command=InventoryMovementFilters(
                    from_date=start_date,
                    to_date=end_date,
                    owner_type=owner_type
                )
            )
        )

        movement_rows = self._build_movement_rows(
            movements
        )

        summaries = self._build_summary_rows(
            movements
        )

        metrics = self._build_metrics(
            movements
        )

        metadata = self._build_metadata(
            owner_type=owner_type,
            start_date=start_date,
            end_date=end_date
        )

        return InventoryMovementReportData(
            metadata=metadata,
            movements=movement_rows,
            material_summaries=summaries,
            metrics=metrics
        )
    
    def _build_movement_rows(
        self,
        movements: list[InventoryMovement]
    ) -> list[InventoryMovementReportRow]:

        return [
            InventoryMovementReportRow(
                movement_date=movement.created_at,

                owner_code=movement.owner_code,
                owner_name=movement.owner_name,

                movement_type=movement.type,
                movement_reason=movement.reason,

                previous_stock=movement.previous_stock,
                quantity=movement.quantity,
                new_stock=movement.new_stock
            )
            for movement in movements
        ]
    
    def _build_summary_rows(
        self,
        movements: list[InventoryMovement]
    ) -> list[InventoryOwnerSummaryRow]:

        summary: dict[int, dict] = {}

        for movement in movements:

            owner_id = movement.owner_id

            if owner_id not in summary:

                summary[owner_id] = {
                    "owner_name": movement.owner_name,
                    "entries": 0,
                    "sales": 0,
                    "customer_returns": 0,
                    "supplier_returns": 0,
                    "manual_positive": 0,
                    "manual_negative": 0,
                    "final_stock": movement.new_stock
                }

            self._accumulate_movement(
                summary[owner_id],
                movement
            )

        return [
            InventoryOwnerSummaryRow(
                owner_id=owner_id,
                owner_name=data["owner_name"],

                total_entries=data["entries"],
                total_sales=data["sales"],

                total_customer_returns=data["customer_returns"],
                total_supplier_returns=data["supplier_returns"],

                manual_adjustment_increase=data["manual_positive"],
                manual_adjustment_decrease=data["manual_negative"],

                final_stock=data["final_stock"],
            )
            for owner_id, data
            in summary.items()
        ]
    
    def _build_metrics(
        self,
        movements: list[InventoryMovement]
    ) -> InventoryReportMetrics:

        metrics = {
            "entries": 0,
            "sales": 0,
            "customer_returns": 0,
            "supplier_returns": 0,
            "manual_positive": 0,
            "manual_negative": 0,
        }

        for movement in movements:
            self._accumulate_movement(
                metrics,
                movement
            )

        affected_owners = len({
            movement.owner_id
            for movement in movements
        })

        return InventoryReportMetrics(
            total_movements=len(movements),

            total_entries=metrics["entries"],
            total_sales=metrics["sales"],

            total_customer_returns=metrics["customer_returns"],
            total_supplier_returns=metrics["supplier_returns"],

            total_manual_adjustment_increase=metrics["manual_positive"],
            total_manual_adjustment_decrease=metrics["manual_negative"],

            affected_owners=affected_owners,
        )
            
    def _build_metadata(
        self,
        *,
        owner_type: InventoryOwnerType,
        start_date: datetime,
        end_date: datetime
    ) -> ReportMetadata:
        return ReportMetadata(
            title=REPORT_CONTEXT_NAMES[
                owner_type
            ],
            start_date=start_date,
            end_date=end_date,
            generated_at=datetime.now()
        )
    
    def _accumulate_movement(
        self,
        accumulator: dict[str, int],
        movement: InventoryMovement
    ) -> None:

        if movement.type == InventoryMovementType.ENTRY:
            accumulator["entries"] += movement.quantity

        elif movement.type == InventoryMovementType.SALE:
            accumulator["sales"] += movement.quantity

        elif movement.type == InventoryMovementType.CUSTOMER_RETURN:
            accumulator["customer_returns"] += movement.quantity

        elif movement.type == InventoryMovementType.SUPPLIER_RETURN:
            accumulator["supplier_returns"] += movement.quantity

        elif movement.type == InventoryMovementType.MANUAL_ADJUSTMENT:

            delta = (
                movement.new_stock
                - movement.previous_stock
            )

            if delta > 0:
                accumulator["manual_positive"] += delta

            elif delta < 0:
                accumulator["manual_negative"] += abs(delta)