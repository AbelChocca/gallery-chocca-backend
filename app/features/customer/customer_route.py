from fastapi import APIRouter

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

from app.features.customer import routes  # noqa: E402,F401