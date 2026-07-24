from app.features.material.entities.material import Material
from app.features.material.dto.material import MaterialFilters
from app.features.material.types import (
    MaterialType,
    UnitType,
)
from app.core.exceptions import (
    ValueNotFound
)
from app.shared.types import CompanyType

from app.infra.db.uow.unit_of_work import UnitOfWork

from datetime import datetime, timezone

import pytest

def build_material(
    **overrides
) -> Material:
    defaults = {
        "id": None,
        "code": "MAT-000001",
        "name": "Material",
        "description": "Material de prueba",
        "company": CompanyType.OLD_DENIM,
        "material_type": MaterialType.FABRIC,
        "unit_type": UnitType.METER,
        "is_active": True,
        "created_at": datetime.now(
            timezone.utc
        ),
        "updated_at": datetime.now(
            timezone.utc
        ),
    }

    defaults.update(overrides)

    return Material(**defaults)

@pytest.mark.asyncio
async def test_should_filter_materials_by_search_text(
    uow_factory
):
    uow: UnitOfWork = uow_factory()
    async with uow:

        await uow.materials.save(
            build_material(
                code="TEL-000001",
                name="Tela Blanca"
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="HIL-000001",
                name="Hilo Negro"
            ),
            flush=False
        )

    uow: UnitOfWork = uow_factory()
    async with uow:

        materials = await uow.materials.get_all(
            filters=MaterialFilters(
                search="Tela"
            )
        )

        assert len(materials) == 1

        assert (
            materials[0].name
            == "Tela Blanca"
        )

        assert (
            materials[0].code
            == "TEL-000001"
        )


@pytest.mark.asyncio
async def test_should_apply_all_filters(
    uow_factory
):
    now = datetime.now(timezone.utc)

    async with uow_factory() as uow:

        # ✅ Debe coincidir
        await uow.materials.save(
            build_material(
                code="TEL-000001",
                name="Tela Blanca",
                company=CompanyType.OLD_DENIM,
                is_active=True,
                created_at=now
            ),
            flush=False
        )

        # ❌ Search
        await uow.materials.save(
            build_material(
                code="HIL-000001",
                name="Hilo Negro",
                company=CompanyType.OLD_DENIM,
                is_active=True,
                created_at=now
            ),
            flush=False
        )

        # ❌ Company
        await uow.materials.save(
            build_material(
                code="TEL-000002",
                name="Tela Azul",
                company=CompanyType.CHOCCA,
                is_active=True,
                created_at=now
            ),
            flush=False
        )

        # ❌ Active
        await uow.materials.save(
            build_material(
                code="TEL-000003",
                name="Tela Roja",
                company=CompanyType.OLD_DENIM,
                is_active=False,
                created_at=now
            ),
            flush=False
        )

        # ❌ Availability (AVAILABLE)
        await uow.materials.save(
            build_material(
                code="TEL-000004",
                name="Tela Verde",
                company=CompanyType.CHOCCA,
                is_active=True,
                created_at=now
            ),
            flush=False
        )

    async with uow_factory() as uow:

        materials = await uow.materials.get_all(
            filters=MaterialFilters(
                search="Tela",
                company=CompanyType.OLD_DENIM,
                is_active=True,
            )
        )

        assert len(materials) == 1

        material = materials[0]

        assert material.code == "TEL-000001"
        assert material.name == "Tela Blanca"

@pytest.mark.asyncio
async def test_should_get_material_by_code(
    uow_factory
):
    async with uow_factory() as uow:

        await uow.materials.save(
            build_material(
                code="TEL-000001",
                name="Tela Blanca"
            ),
            flush=False
        )

    async with uow_factory() as uow:

        material = await (
            uow.materials.get_by_code(
                "TEL-000001"
            )
        )

        assert material.code == "TEL-000001"
        assert material.name == "Tela Blanca"

@pytest.mark.asyncio
async def test_should_raise_error_when_material_code_does_not_exist(
    uow_factory
):
    uow: UnitOfWork = uow_factory()

    async with uow:

        with pytest.raises(
            ValueNotFound,
            match="Material not found."
        ):
            await uow.materials.get_by_code(
                "NOT-FOUND"
            )

@pytest.mark.asyncio
async def test_should_get_materials_by_ids(
    uow_factory
):
    uow: UnitOfWork = uow_factory()
    async with uow:

        material_1 = build_material(
            code="TEL-000001"
        )

        material_2 = build_material(
            code="TEL-000002"
        )

        material_3 = build_material(
            code="TEL-000003"
        )

        material_1 = await uow.materials.save(
            material_1,
        )

        material_2 = await uow.materials.save(
            material_2,
        )

        material_3 = await uow.materials.save(
            material_3
        )

    uow: UnitOfWork = uow_factory()

    async with uow:

        materials = await (
            uow.materials.get_by_ids(
                [
                    material_1.id,
                    material_3.id
                ]
            )
        )

        assert len(materials) == 2

        ids = {
            material.id
            for material in materials
        }

        assert material_1.id in ids
        assert material_3.id in ids

@pytest.mark.asyncio
async def test_should_return_empty_list_when_ids_are_empty(
    uow_factory
):
    uow: UnitOfWork = uow_factory()

    async with uow:

        materials = await (
            uow.materials.get_by_ids([])
        )

        assert materials == []