import pytest
from decimal import Decimal

from app.features.material.service import MaterialService
from app.features.material.dto.material import CreateMaterialDTO, UpdateMaterialDTO
from app.core.exceptions import ValidationError

from app.features.material.types import (
    CompanyType,
    MaterialType,
    UnitType
)

@pytest.mark.asyncio
async def test_should_create_material(material_service: MaterialService):

    dto = CreateMaterialDTO(
        name="Tela Blanca",
        description="Algodón premium",
        company=CompanyType.OLD_DENIM,
        minimum_stock=20,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.METER
    )

    result = await material_service.create(dto)

    assert result.id is not None

    assert result.name == "Tela Blanca"
    assert result.description == "Algodón premium"
    assert result.company == CompanyType.OLD_DENIM

    assert result.stock == 0
    assert result.minimum_stock == 20
    assert result.is_active is True

    assert result.code.startswith("TBX-")

@pytest.mark.asyncio
async def test_should_not_create_material_when_name_already_exists(
    material_service: MaterialService
):

    dto = CreateMaterialDTO(
        name="Tela Blanca",
        description="Algodón premium",
        company=CompanyType.OLD_DENIM,
        minimum_stock=20,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.METER
    )

    await material_service.create(dto)

    duplicate_dto = CreateMaterialDTO(
        name="Tela Blanca",
        description="Otro producto",
        company=CompanyType.CHOCCA,
        minimum_stock=10,
        material_type=MaterialType.ACCESSORY,
        unit_type=UnitType.UNIT
    )

    with pytest.raises(ValidationError) as exc:
        await material_service.create(duplicate_dto)

    assert "already exists" in str(exc.value)

async def test_should_generate_incremental_code_sequence(
    material_service: MaterialService
):
    first_material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Blanca",
            minimum_stock=10,
            description=None,
            company=CompanyType.OLD_DENIM,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER
        )
    )

    second_material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Negra",
            minimum_stock=10,
            description=None,
            company=CompanyType.OLD_DENIM,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER
        )
    )

    first_sequence = int(first_material.code.split("-")[1])
    second_sequence = int(second_material.code.split("-")[1])

    assert second_sequence == first_sequence + 1

async def test_should_update_material_information(
    material_service: MaterialService
):
    created_material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Blanca",
            description="Tela para camisas",
            company=CompanyType.OLD_DENIM,
            minimum_stock=20,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER
        )
    )

    await material_service.update(
        created_material.id,
        UpdateMaterialDTO(
            name="Tela Premium",
            description="Tela premium importada",
            company=CompanyType.CHOCCA,
            minimum_stock=50
        )
    )

    updated_material = await material_service.get_by_id(
        created_material.id
    )

    assert updated_material.name == "Tela Premium"
    assert updated_material.description == "Tela premium importada"
    assert updated_material.company == CompanyType.CHOCCA
    assert updated_material.minimum_stock == 50
    assert not updated_material.code.startswith("TBX")

async def test_should_regenerate_code_prefix_when_name_changes(
    material_service: MaterialService
):
    created_material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Blanca",
            minimum_stock=20,
            description=None,
            company=CompanyType.OLD_DENIM,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER
        )
    )

    original_code = created_material.code

    await material_service.update(
        created_material.id,
        UpdateMaterialDTO(
            name="Hilo Negro",
            minimum_stock=20,
            company=CompanyType.OLD_DENIM,
            description=None
        )
    )

    updated_material = await material_service.get_by_id(
        created_material.id
    )

    assert updated_material.code != original_code
    assert updated_material.code.startswith("HNX")

async def test_should_return_paginated_materials(
    material_service: MaterialService
):
    for i in range(15):
        await material_service.create(
            CreateMaterialDTO(
                name=f"Tela {i}",
                minimum_stock=10,
                description=None,
                company=CompanyType.OLD_DENIM,
                material_type=MaterialType.FABRIC,
                unit_type=UnitType.METER
            )
        )

    first_page = await material_service.get_all(
        page=1,
        limit=10
    )

    second_page = await material_service.get_all(
        page=2,
        limit=10
    )

    assert len(first_page.items) == 10
    assert len(second_page.items) == 5
