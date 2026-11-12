import uuid

import pytest
import pytest_asyncio

from app.features.locations.models.ubigeo import UbigeoTable
from app.features.locations.types import LocationType

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def location_ubigeo(db_session):
    code = f"8{uuid.uuid4().int % 100000:05d}"

    ubigeo = UbigeoTable(
        code=code,
        department="LIMA",
        province="LIMA",
        district="LA VICTORIA",
        city_name="LIMA",
    )

    db_session.add(ubigeo)

    await db_session.commit()
    await db_session.refresh(ubigeo)

    return ubigeo


@pytest.fixture
def location_payload(location_ubigeo):
    suffix = uuid.uuid4().hex[:8]

    return {
        "name": f"CHOCCA E2E - Tienda {suffix}",
        "type": LocationType.STORE.value,
        "address": "Av. Gamarra 123, La Victoria",
        "ubigeo_code": location_ubigeo.code,
        "latitude": "-12.064500",
        "longitude": "-77.012300",
        "phone": "999999999",
        "reference": "Local de pruebas E2E",
        "is_active": True,
        "pickup_enabled": True,
    }

