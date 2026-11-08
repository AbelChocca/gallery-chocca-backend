from fastapi import APIRouter

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)

from app.features.complaints import routes  # noqa: E402,F401