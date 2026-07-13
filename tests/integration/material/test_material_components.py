import pytest
from decimal import Decimal

from app.features.material.service import MaterialService
from app.features.material.dto.material import CreateMaterialDTO, UpdateMaterialDTO
from app.core.exceptions import ValidationError

from app.features.material.dto.material_component import CreateMaterialComponentDTO
from app.features.material.types import (
    CompanyType,
    MaterialType,
    UnitType,
    FiberType,
)

@pytest.mark.asyncio
async def test_should_create_material_with_components(
    material_service: MaterialService
):
    material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Jersey",
            description=None,
            company=CompanyType.OLD_DENIM,
            minimum_stock=10,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER,
            components=[
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.COTTON,
                    percentage=Decimal("80"),
                ),
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.POLYESTER,
                    percentage=Decimal("20")
                )
            ]
        )
    )

    created_material = await material_service.get_by_id(
        material.id
    )

    assert len(created_material.components) == 2

    assert (
        created_material.components[0].fiber_type
        == FiberType.COTTON
    )
    assert (
        created_material.components[0].percentage
        == Decimal("80")
    )

    assert (
        created_material.components[1].fiber_type
        == FiberType.POLYESTER
    )
    assert (
        created_material.components[1].percentage
        == Decimal("20")
    )

@pytest.mark.asyncio
async def test_should_remove_all_components_when_updating_with_empty_list(
    material_service: MaterialService
):
    material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Jersey",
            description=None,
            company=CompanyType.OLD_DENIM,
            minimum_stock=10,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER,
            components=[
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.COTTON,
                    percentage=Decimal("100")
                )
            ]
        )
    )

    await material_service.update(
        material.id,
        UpdateMaterialDTO(
            components=[]
        )
    )

    updated_material = await material_service.get_by_id(
        material.id
    )

    assert updated_material.components == []

@pytest.mark.asyncio
async def test_should_replace_existing_components(
    material_service: MaterialService
):
    material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Jersey",
            description=None,
            company=CompanyType.OLD_DENIM,
            minimum_stock=10,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER,
            components=[
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.COTTON,
                    percentage=Decimal("80")
                ),
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.POLYESTER,
                    percentage=Decimal("20")
                )
            ]
        )
    )

    await material_service.update(
        material.id,
        UpdateMaterialDTO(
            components=[
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.VISCOSE,
                    percentage=Decimal("60")
                ),
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.LINEN,
                    percentage=Decimal("40")
                )
            ]
        )
    )

    updated_material = await material_service.get_by_id(
        material.id
    )

    assert len(updated_material.components) == 2

    fiber_types = {
        c.fiber_type
        for c in updated_material.components
    }

    percentages = {
        c.percentage
        for c in updated_material.components
    }

    assert FiberType.VISCOSE in fiber_types
    assert FiberType.LINEN in fiber_types

    assert Decimal("60") in percentages
    assert Decimal("40") in percentages

@pytest.mark.asyncio
async def test_should_not_create_components_for_non_fabric_material(
    material_service: MaterialService
):
    dto = CreateMaterialDTO(
        name="Botón Negro",
        description=None,
        company=CompanyType.OLD_DENIM,
        minimum_stock=10,
        material_type=MaterialType.ACCESSORY,
        unit_type=UnitType.UNIT,
        components=[
            CreateMaterialComponentDTO(
                fiber_type=FiberType.COTTON,
                percentage=Decimal("100")
            )
        ]
    )

    with pytest.raises(ValidationError) as exc:
        await material_service.create(dto)

    assert "no pueden asociarse" in str(exc.value)

@pytest.mark.asyncio
async def test_should_not_create_component_with_non_positive_percentage(
    material_service: MaterialService
):
    dto = CreateMaterialDTO(
        name="Tela Jersey",
        description=None,
        company=CompanyType.OLD_DENIM,
        minimum_stock=10,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.METER,
        components=[
            CreateMaterialComponentDTO(
                fiber_type=FiberType.COTTON,
                percentage=Decimal("0")
            )
        ]
    )

    with pytest.raises(ValidationError) as exc:
        await material_service.create(dto)

    assert "mayor a 0" in str(exc.value)

@pytest.mark.asyncio
async def test_should_not_create_components_when_total_percentage_is_not_100(
    material_service: MaterialService
):
    dto = CreateMaterialDTO(
        name="Tela Jersey",
        description=None,
        company=CompanyType.OLD_DENIM,
        minimum_stock=10,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.METER,
        components=[
            CreateMaterialComponentDTO(
                fiber_type=FiberType.COTTON,
                percentage=Decimal("70")
            ),
            CreateMaterialComponentDTO(
                fiber_type=FiberType.POLYESTER,
                percentage=Decimal("20")
            )
        ]
    )

    with pytest.raises(ValidationError) as exc:
        await material_service.create(dto)

    assert "exactamente 100" in str(exc.value)

@pytest.mark.asyncio
async def test_should_not_create_components_with_duplicate_fiber_types(
    material_service: MaterialService
):
    dto = CreateMaterialDTO(
        name="Tela Jersey",
        description=None,
        company=CompanyType.OLD_DENIM,
        minimum_stock=10,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.METER,
        components=[
            CreateMaterialComponentDTO(
                fiber_type=FiberType.COTTON,
                percentage=Decimal("50")
            ),
            CreateMaterialComponentDTO(
                fiber_type=FiberType.COTTON,
                percentage=Decimal("50")
            )
        ]
    )

    with pytest.raises(ValidationError) as exc:
        await material_service.create(dto)

    assert "No se pueden repetir" in str(exc.value)

@pytest.mark.asyncio
async def test_should_get_material_with_components_mapped(
    material_service: MaterialService
):
    created = await material_service.create(
        CreateMaterialDTO(
            name="Tela Piqué",
            description="Tela de prueba",
            company=CompanyType.OLD_DENIM,
            minimum_stock=10,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER,
            components=[
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.COTTON,
                    percentage=Decimal("70"),
                ),
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.POLYESTER,
                    percentage=Decimal("30"),
                ),
            ],
        )
    )

    material = await material_service.get_by_id(created.id)

    assert material.id == created.id
    assert material.name == "Tela Piqué"
    assert material.material_type == MaterialType.FABRIC

    assert material.components is not None
    assert len(material.components) == 2

    components = {
        component.fiber_type: component.percentage
        for component in material.components
    }

    assert components == {
        FiberType.COTTON: Decimal("70"),
        FiberType.POLYESTER: Decimal("30"),
    }

@pytest.mark.asyncio
async def test_should_remove_components_when_material_changes_to_non_fabric(
    material_service: MaterialService
):
    material = await material_service.create(
        CreateMaterialDTO(
            name="Tela Jersey",
            description=None,
            company=CompanyType.OLD_DENIM,
            minimum_stock=10,
            material_type=MaterialType.FABRIC,
            unit_type=UnitType.METER,
            components=[
                CreateMaterialComponentDTO(
                    fiber_type=FiberType.COTTON,
                    percentage=Decimal("100"),
                )
            ],
        )
    )

    await material_service.update(
        material.id,
        UpdateMaterialDTO(
            material_type=MaterialType.ACCESSORY,
        ),
    )

    updated = await material_service.get_by_id(
        material.id
    )

    assert updated.material_type == MaterialType.ACCESSORY
    assert updated.components == []