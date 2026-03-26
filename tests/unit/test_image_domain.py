# test_image_domain.py
import pytest
from app.domain.media.entities.image import ImageEntity
from app.core.exceptions import ValidationError

# -------------------------
# 1️⃣ Test de creación básica
# -------------------------
def test_image_entity_creation():
    image = ImageEntity(
        image_url="http://image.com/img.jpg",
        owner_type="variant",
        public_id="img_123"
    )
    assert image.image_url == "http://image.com/img.jpg"
    assert image.public_id == "img_123"
    assert image.owner_type == "variant"
    assert image.owner_id is None
    assert image.id is None
    assert image.alt_text is None

# ------------------------------------
# 2️⃣ Test setter de public_id
# ------------------------------------
def test_set_public_id():
    image = ImageEntity("url", "variant", "img_123")
    
    # correcto
    image.public_id = "img_456"
    assert image.public_id == "img_456"
    
    # incorrecto
    with pytest.raises(ValidationError):
        image.public_id = 123  # no string

# ------------------------------
# 3️⃣ Test setters de owner_id y id
# ------------------------------
def test_set_owner_and_id():
    image = ImageEntity("url", "variant", "img_123")
    
    image.owner_id = 99
    image.id = 1001
    
    assert image.owner_id == 99
    assert image.id == 1001

# ------------------------------
# 4️⃣ Test set_alt_text
# ------------------------------
def test_set_alt_text():
    image = ImageEntity("url", "variant", "img_123")
    
    # correcto
    image.set_alt_text({"en": "Front view", "es": "Vista frontal"})
    assert image.alt_text == "Front view Vista frontal"
    
    # args no es dict
    with pytest.raises(ValidationError):
        image.set_alt_text("not a dict")
    
    # value no es string
    with pytest.raises(ValidationError):
        image.set_alt_text({"en": 123})

# ------------------------------
# 5️⃣ Test validate_image_attr
# ------------------------------
def test_validate_image_attr():
    with pytest.raises(ValidationError):
        image_empty_url = ImageEntity("", "variant", "img_123")
    
    with pytest.raises(ValidationError):
        # public_id vacío
        image_empty_id = ImageEntity("url", "variant", "")

# ------------------------------
# 6️⃣ Test to_dict
# ------------------------------
def test_image_to_dict():
    image = ImageEntity(
        "url", "variant", "img_123", owner_id=1, id=10, alt_text="alt"
    )
    d = image.to_dict
    assert d["image_url"] == "url"
    assert d["owner_type"] == "variant"
    assert d["public_id"] == "img_123"
    assert d["owner_id"] == 1
    assert d["id"] == 10
    assert d["alt_text"] == "alt"