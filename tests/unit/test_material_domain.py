from datetime import datetime, timezone

import pytest

from app.features.material.entities.material import Material

from app.features.material.types import (
    CompanyType,
    MaterialType,
    UnitType
)

from app.features.material.types import (
    MaterialAvailabilityStatus
)


@pytest.fixture
def make_material():
    def _make_material(**overrides):
        defaults = {
            "id": 1,
            "code": "ALG-000001",
            "name": "Algodón",
            "description": "Algodón premium",
            "company": CompanyType.OLD_DENIM,
            "stock": 100,
            "minimum_stock": 20,
            "material_type": MaterialType.FABRIC,
            "unit_type": UnitType.METER,
            "is_active": True,
            "created_at": datetime(
                2026, 1, 1,
                tzinfo=timezone.utc
            ),
            "updated_at": datetime(
                2026, 1, 1,
                tzinfo=timezone.utc
            ),
        }

        defaults.update(overrides)

        return Material(**defaults)

    return _make_material


def test_should_create_material_with_provided_values(
    make_material
):
    material = make_material()

    assert material.id == 1
    assert material.code == "ALG-000001"
    assert material.name == "Algodón"
    assert material.description == "Algodón premium"

    assert material.company == CompanyType.OLD_DENIM

    assert material.stock == 100
    assert material.minimum_stock == 20

    assert (
        material.material_type
        == MaterialType.FABRIC
    )

    assert (
        material.unit_type
        == UnitType.METER
    )

    assert material.is_active is True


def test_should_generate_created_and_updated_at_when_not_provided():
    before_creation = datetime.now(
        timezone.utc
    )

    material = Material(
        id=1,
        code="ALG-000001",
        name="Algodón",
        description="Algodón premium",
        company=CompanyType.OLD_DENIM,
        stock=100,
        minimum_stock=20,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.METER,
        is_active=True,
    )

    after_creation = datetime.now(
        timezone.utc
    )

    assert material.created_at is not None
    assert material.updated_at is not None

    assert (
        before_creation
        <= material.created_at
        <= after_creation
    )

    assert (
        before_creation
        <= material.updated_at
        <= after_creation
    )

def test_should_return_out_of_stock_when_stock_is_zero(
    make_material
):
    material = make_material(
        stock=0
    )

    assert (
        material.availability_status
        == MaterialAvailabilityStatus.OUT_OF_STOCK
    )


def test_should_return_critical_when_stock_is_less_or_equal_minimum_stock(
    make_material
):
    material = make_material(
        stock=20,
        minimum_stock=20
    )

    assert (
        material.availability_status
        == MaterialAvailabilityStatus.CRITICAL
    )


def test_should_return_available_when_stock_is_greater_than_minimum_stock(
    make_material
):
    material = make_material(
        stock=21,
        minimum_stock=20
    )

    assert (
        material.availability_status
        == MaterialAvailabilityStatus.AVAILABLE
    )

def test_should_update_material_information(
    make_material
):
    material = make_material()

    material.update_information(
        name="Raw Cotton",
        description="New description",
        company=CompanyType.OLD_DENIM,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.KILOGRAM,
        minimum_stock=50
    )

    assert material.name == "Raw Cotton"
    assert material.description == "New description"
    assert material.company == CompanyType.OLD_DENIM

    assert (
        material.material_type
        == MaterialType.FABRIC
    )

    assert (
        material.unit_type
        == UnitType.KILOGRAM
    )

    assert material.minimum_stock == 50

def test_should_update_updated_at_when_information_changes(
    make_material
):
    material = make_material()

    previous_updated_at = (
        material.updated_at
    )

    material.update_information(
        name="Raw Cotton",
        description="New description",
        company=CompanyType.OLD_DENIM,
        material_type=MaterialType.FABRIC,
        unit_type=UnitType.KILOGRAM,
        minimum_stock=50
    )

    assert (
        material.updated_at
        > previous_updated_at
    )

def test_should_deactivate_material(
    make_material
):
    material = make_material(
        is_active=True
    )

    material.deactivate()

    assert material.is_active is False

def test_should_activate_material(
    make_material
):
    material = make_material(
        is_active=False
    )

    material.activate()

    assert material.is_active is True

def test_should_build_code_with_three_letter_prefix():
    code = Material.build_code(
        "Cotton Thread",
        15
    )

    assert code == "CTX-000015"

def test_should_pad_prefix_with_x_when_name_has_less_than_three_initials():
    code = Material.build_code(
        "Ink",
        1
    )

    assert code == "IXX-000001"

def test_should_regenerate_prefix_using_current_name(
    make_material
):
    material = make_material(
        code="ABC-000123",
        name="Raw Cotton"
    )

    material.regenerate_code_prefix()

    assert material.code.startswith(
        "RCX"
    )

    assert (
        material.code
        == "RCX-000123"
    )

def test_should_update_updated_at_when_regenerating_code_prefix(
    make_material
):
    material = make_material(
        name="Raw Cotton"
    )

    previous_updated_at = (
        material.updated_at
    )

    material.regenerate_code_prefix()

    assert (
        material.updated_at
        > previous_updated_at
    )