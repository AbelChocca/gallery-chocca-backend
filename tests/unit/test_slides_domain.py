# test_slide_domain.py
import pytest
from datetime import datetime
from app.domain.media.entities.image import ImageEntity
from app.domain.slide.slide_entity import SlideEntity
from app.core.exceptions import ValidationError, ValueNotFound

# ------------------------
# 1️⃣ Test creación básica
# ------------------------
def test_slide_entity_creation():
    slide = SlideEntity(id=1, activo=True, orden=1, enlace_boton="http://link.com")
    assert slide.id == 1
    assert slide.activo is True
    assert slide.orden == 1
    assert slide.enlace_boton == "http://link.com"
    assert isinstance(slide.fecha_creada, datetime)
    assert isinstance(slide.fecha_actualizada, datetime)
    assert slide.has_image is False

# ------------------------
# 2️⃣ Test setter de orden
# ------------------------
def test_set_valid_order():
    slide = SlideEntity(orden=1)
    slide.orden = 5
    assert slide.orden == 5

def test_set_invalid_order_type():
    slide = SlideEntity(orden=1)
    with pytest.raises(ValidationError):
        slide.orden = "not an int"

def test_set_invalid_order_value():
    slide = SlideEntity(orden=1)
    with pytest.raises(ValidationError):
        slide.orden = 0  # <= 0 no permitido

# ------------------------
# 3️⃣ Test setter de image
# ------------------------
def test_set_image_entity():
    slide = SlideEntity()
    image = ImageEntity("url", "slide", "img_123")
    slide.image = image
    assert slide.has_image is True
    assert slide.image_public_id == "img_123"

def test_set_image_invalid_type():
    slide = SlideEntity()
    with pytest.raises(ValidationError):
        slide.image = "not an image entity"

def test_set_image_none():
    slide = SlideEntity()
    slide.image = None
    assert slide.has_image is False

# ------------------------
# 4️⃣ Test sync_image
# ------------------------
def test_sync_image_success():
    slide = SlideEntity(id=1)
    image = ImageEntity("url", "slide", "img_123")
    slide.sync_image({1: image})
    assert slide.image == image

def test_sync_image_not_found():
    slide = SlideEntity(id=1)
    with pytest.raises(ValueNotFound):
        slide.sync_image({2: ImageEntity("url", "slide", "img_999")})

# ------------------------
# 5️⃣ Test toggle_activation
# ------------------------
def test_toggle_activation():
    slide = SlideEntity(activo=True)
    slide.toggle_activation(False)
    assert slide.activo is False
    slide.toggle_activation(True)
    assert slide.activo is True

# ------------------------
# 6️⃣ Test update_slide
# ------------------------
def test_update_slide_basic():
    slide = SlideEntity(id=1, activo=True, orden=1, enlace_boton="http://link.com")
    old_timestamp = slide.fecha_actualizada
    slide.update_slide({"activo": False, "orden": 5, "enlace_boton": "http://nuevo.com"})
    
    assert slide.activo is False
    assert slide.orden == 5
    assert slide.enlace_boton == "http://nuevo.com"
    assert slide.fecha_actualizada > old_timestamp

def test_update_slide_invalid_obj():
    slide = SlideEntity()
    with pytest.raises(ValidationError):
        slide.update_slide("not a dict")

def test_update_slide_empty_obj():
    slide = SlideEntity()
    with pytest.raises(ValidationError):
        slide.update_slide({})