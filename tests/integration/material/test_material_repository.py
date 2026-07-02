from datetime import datetime, timezone

import pytest

from app.features.material.entity import Material
from app.features.material.dto import MaterialFilters
from app.features.material.types import (
    CompanyType,
    MaterialType,
    UnitType,
    MaterialAvailabilityStatus
)

from app.infra.db.uow.unit_of_work import UnitOfWork

def build_material(
    **overrides
) -> Material:
    defaults = {
        "id": None,
        "code": "MAT-000001",
        "name": "Material",
        "description": "Material de prueba",
        "company": CompanyType.OLD_DENIM,
        "stock": 100,
        "minimum_stock": 20,
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
async def test_should_return_only_critical_materials(
    uow_factory
):
    async with uow_factory() as uow:

        await uow.materials.save(
            build_material(
                code="TEL-000001",
                name="Tela Critica",
                stock=10,
                minimum_stock=20
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="TEL-000002",
                name="Tela Sin Stock",
                stock=0,
                minimum_stock=20
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="TEL-000003",
                name="Tela Disponible",
                stock=50,
                minimum_stock=20
            ),
            flush=False
        )

    async with uow_factory() as uow:

        materials = await uow.materials.get_all(
            filters=MaterialFilters(
                availability_status=(
                    MaterialAvailabilityStatus.CRITICAL
                )
            )
        )

        assert len(materials) == 1
        assert materials[0].code == "TEL-000001"
        assert materials[0].name == "Tela Critica"

@pytest.mark.asyncio
async def test_should_return_only_out_of_stock_materials(
    uow_factory
):
    async with uow_factory() as uow:

        await uow.materials.save(
            build_material(
                code="TEL-000001",
                name="Tela Sin Stock",
                stock=0,
                minimum_stock=20
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="TEL-000002",
                name="Tela Critica",
                stock=10,
                minimum_stock=20
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="TEL-000003",
                name="Tela Disponible",
                stock=50,
                minimum_stock=20
            ),
            flush=False
        )

    async with uow_factory() as uow:

        materials = await uow.materials.get_all(
            filters=MaterialFilters(
                availability_status=
                MaterialAvailabilityStatus.OUT_OF_STOCK
            )
        )

        assert len(materials) == 1
        assert materials[0].code == "TEL-000001"
        assert materials[0].name == "Tela Sin Stock"

@pytest.mark.asyncio
async def test_should_return_only_available_materials(
    uow_factory
):
    async with uow_factory() as uow:

        await uow.materials.save(
            build_material(
                code="TEL-000001",
                name="Tela Disponible",
                stock=50,
                minimum_stock=20
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="TEL-000002",
                name="Tela Critica",
                stock=10,
                minimum_stock=20
            ),
            flush=False
        )

        await uow.materials.save(
            build_material(
                code="TEL-000003",
                name="Tela Sin Stock",
                stock=0,
                minimum_stock=20
            ),
            flush=False
        )

    async with uow_factory() as uow:

        materials = await uow.materials.get_all(
            filters=MaterialFilters(
                availability_status=
                MaterialAvailabilityStatus.AVAILABLE
            )
        )

        assert len(materials) == 1
        assert materials[0].code == "TEL-000001"
        assert materials[0].name == "Tela Disponible"


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
                stock=10,
                minimum_stock=20,
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
                stock=10,
                minimum_stock=20,
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
                stock=10,
                minimum_stock=20,
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
                stock=10,
                minimum_stock=20,
                created_at=now
            ),
            flush=False
        )

        # ❌ Availability (AVAILABLE)
        await uow.materials.save(
            build_material(
                code="TEL-000004",
                name="Tela Verde",
                company=CompanyType.OLD_DENIM,
                is_active=True,
                stock=50,
                minimum_stock=20,
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
                availability_status=(
                    MaterialAvailabilityStatus.CRITICAL
                )
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

from app.core.exceptions import (
    ValueNotFound
)


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

@pytest.mark.asyncio
async def test_should_update_material_stock(
    uow_factory
):
    uow: UnitOfWork = uow_factory()
    async with uow:

        material = build_material(
            stock=100
        )

        material = await uow.materials.save(material)

        material_id = material.id

    uow: UnitOfWork = uow_factory()
    async with uow:

        await uow.materials.update_stock(
            material_id=material_id,
            new_stock=50
        )

    uow: UnitOfWork = uow_factory()
    async with uow:

        updated_material = (
            await uow.materials.get_by_id(
                material_id
            )
        )

        assert updated_material.stock == 50

@pytest.mark.asyncio
async def test_should_update_many_material_stocks(
    uow_factory
):
    uow: UnitOfWork = uow_factory()
    async with uow:

        material_1 = build_material(
            code="MAT-000001",
            stock=100
        )

        material_2 = build_material(
            code="MAT-000002",
            stock=200
        )

        material_3 = build_material(
            code="MAT-000003",
            stock=300
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

        material_1_id = material_1.id
        material_2_id = material_2.id
        material_3_id = material_3.id

    uow: UnitOfWork = uow_factory()
    async with uow:

        await uow.materials.update_stock_many(
            {
                material_1_id: 10,
                material_2_id: 20,
                material_3_id: 30
            }
        )

    uow: UnitOfWork = uow_factory()
    async with uow:

        materials = await (
            uow.materials.get_by_ids(
                [
                    material_1_id,
                    material_2_id,
                    material_3_id
                ]
            )
        )

        materials_by_id = {
            material.id: material
            for material in materials
        }

        assert (
            materials_by_id[
                material_1_id
            ].stock
            == 10
        )

        assert (
            materials_by_id[
                material_2_id
            ].stock
            == 20
        )

        assert (
            materials_by_id[
                material_3_id
            ].stock
            == 30
        )