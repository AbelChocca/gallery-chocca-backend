import pytest

from app.features.inventory.dto import (
    CreateBulkMovementCommand,
    MovementItem,
)
from app.features.inventory.types import InventoryMovementType
from app.features.material.dto import CreateMaterialDTO
from tests.factories.material_factory import build_material


@pytest.mark.asyncio
async def test_should_update_material_stock(
    material_owner_resolver,
    material_service,
):
    dto = build_material()

    material = await material_service.create(
        CreateMaterialDTO(
            name=dto.name,
            description=dto.description,
            company=dto.company,
            minimum_stock=dto.minimum_stock,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
        )
    )

    owner, previous_stock = (
        await material_owner_resolver.update_stock(
            owner_id=material.id,
            quantity=5,
            movement_type=InventoryMovementType.ENTRY,
        )
    )

    assert previous_stock == 0
    assert owner.id == material.id
    assert owner.stock == 5
    assert owner.name == material.name
    assert owner.code == material.code


@pytest.mark.asyncio
async def test_should_reduce_material_stock(
    material_owner_resolver,
    material_service,
):
    dto = build_material(name="Lino")

    material = await material_service.create(
        CreateMaterialDTO(
            name=dto.name,
            description=dto.description,
            company=dto.company,
            minimum_stock=dto.minimum_stock,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
        )
    )

    await material_service.update_stock(
        material_id=material.id,
        quantity=20,
        movement_type=InventoryMovementType.ENTRY,
    )

    owner, previous_stock = (
        await material_owner_resolver.update_stock(
            owner_id=material.id,
            quantity=7,
            movement_type=InventoryMovementType.SALE,
        )
    )

    assert previous_stock == 20
    assert owner.stock == 13
    assert owner.id == material.id


@pytest.mark.asyncio
async def test_should_update_many_materials(
    material_owner_resolver,
    material_service,
):
    dto1 = build_material(name="Algodón")
    dto2 = build_material(name="Lino")

    material1 = await material_service.create(
        CreateMaterialDTO(
            name=dto1.name,
            description=dto1.description,
            company=dto1.company,
            minimum_stock=dto1.minimum_stock,
            material_type=dto1.material_type,
            unit_type=dto1.unit_type,
        )
    )

    material2 = await material_service.create(
        CreateMaterialDTO(
            name=dto2.name,
            description=dto2.description,
            company=dto2.company,
            minimum_stock=dto2.minimum_stock,
            material_type=dto2.material_type,
            unit_type=dto2.unit_type,
        )
    )

    await material_service.update_stock(
        material_id=material1.id,
        quantity=10,
        movement_type=InventoryMovementType.ENTRY,
    )

    await material_service.update_stock(
        material_id=material2.id,
        quantity=30,
        movement_type=InventoryMovementType.ENTRY,
    )

    command = CreateBulkMovementCommand(
        owner_type="MATERIAL",
        type=InventoryMovementType.ENTRY,
        items=[
            MovementItem(
                owner_id=material1.id,
                quantity=5,
            ),
            MovementItem(
                owner_id=material2.id,
                quantity=10,
            ),
        ],
    )

    result = await material_owner_resolver.update_stock_many(command)

    assert len(result) == 2

    assert result[0].owner_id == material1.id
    assert result[0].previous_stock == 10
    assert result[0].new_stock == 15

    assert result[1].owner_id == material2.id
    assert result[1].previous_stock == 30
    assert result[1].new_stock == 40