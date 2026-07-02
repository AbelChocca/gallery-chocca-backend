from fastapi import APIRouter

router = APIRouter(prefix='/reports', tags=['reports'])

from app.features.reports.routes import generate_inventory_movements_report_excel