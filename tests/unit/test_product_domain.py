# tests/test_product_domain.py
import pytest
from app.domain.product.entities.product import Product
from app.domain.product.entities.product_variant import ProductVariant
from app.domain.product.entities.variant_size import VariantSize
from app.domain.media.entities.image import ImageEntity
from app.core.exceptions import ValidationError

# -----------------------
# Fixtures
# -----------------------
@pytest.fixture
def sample_size():
    return VariantSize(size="M", id=1, variant_id=1)

@pytest.fixture
def sample_image():
    return ImageEntity(image_url="http://image.com/1.jpg", owner_type="variant", public_id="img_1", id=1)

@pytest.fixture
def sample_variant(sample_size, sample_image):
    variant = ProductVariant(color="Red", sizes=[sample_size], id=1, product_id=1)
    variant.agregar_image(sample_image)
    return variant

@pytest.fixture
def sample_product(sample_variant):
    return Product(
        nombre="Camiseta",
        descripcion="Camiseta roja talla M",
        categoria="Ropa",
        slug="camiseta-roja",
        variants=[sample_variant],
        model_family="Summer2026",
        marca="MarcaX",
        fit="Regular"
    )

# -----------------------
# 1️⃣ Product tests
# -----------------------
def test_create_product_valid(sample_product):
    assert sample_product.nombre == "Camiseta"
    assert sample_product.has_variants
    assert sample_product.slug == "camiseta-roja"

def test_create_product_invalid_name():
    with pytest.raises(ValidationError):
        Product(
            nombre="     ",
            descripcion="Desc",
            categoria="Ropa",
            slug="slug",
            variants=[],
            model_family="MF",
            marca="MarcaX"
        )

def test_add_variant_with_images(sample_product):
    new_variant = ProductVariant(color="Blue")
    new_image = ImageEntity(image_url="http://image.com/2.jpg", owner_type="variant", public_id="img_2")
    new_variant.agregar_image(new_image)
    sample_product.add_variant(color="Blue", sizes=["L"], images=[new_image])
    assert sample_product.variants[-1].has_images
    assert sample_product.variants[-1].color == "Blue"

def test_add_variant_without_images(sample_product):
    with pytest.raises(ValidationError):
        sample_product.add_variant(color="Green", sizes=["L"], images=[])

# -----------------------
# 2️⃣ ProductVariant tests
# -----------------------
def test_create_variant_valid(sample_variant):
    assert sample_variant.color == "Red"
    assert sample_variant.has_sizes
    assert sample_variant.has_images

def test_variant_color_validation():
    with pytest.raises(ValidationError):
        ProductVariant(color="#123ABC")
    with pytest.raises(ValidationError):
        ProductVariant(color="Red3")
    with pytest.raises(ValidationError):
        ProductVariant(color="  ")

def test_variant_add_and_sync_images(sample_variant):
    new_image = ImageEntity(id=10, image_url="http://image.com/3.jpg", owner_type="variant", public_id="img_3")
    sample_variant.agregar_image(new_image)
    ids = [img.id for img in sample_variant.imagenes]
    assert 10 in ids

# -----------------------
# 3️⃣ VariantSize tests
# -----------------------
def test_create_variant_size_valid(sample_size):
    assert sample_size.size == "M"
    assert sample_size.variant_id == 1

def test_variant_size_to_dict(sample_size):
    d = sample_size.to_dict
    assert d["size"] == "M"
    assert d["variant_id"] == 1

def test_update_product_and_sync_existing_variants(sample_product):
    # actualizar nombre y model_family
    sample_product.update_product({"nombre": "Camiseta Nueva", "model_family": "Winter2026"})
    assert sample_product.nombre == "Camiseta Nueva"
    assert sample_product.model_family == "Winter2026"
    # actualizar variante
    class DummySizeCommand:
        def __init__(self, id, size):
            self.id = id
            self.size = size
            self.to_delete = False

    class DummyVariantDTO:
        def __init__(self, id):
            self.id = id
            self.to_delete = False
            self.color = "Red Updated"
            self.sizes = [DummySizeCommand(id=2, size="XL")]

    sample_product.sync_existing_variants([DummyVariantDTO(id=1)])
    variant = sample_product.variants[0]
    assert variant.color == "Red Updated"
    assert any(s.size == "XL" for s in variant.sizes)