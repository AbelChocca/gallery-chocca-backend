
from dataclasses import dataclass, field
from uuid import uuid4

import pytest

from app.features.media.service import MediaService
from app.infra.cache.redis_service import RedisService


@dataclass
class FakeProductMedia:
    uploads: list = field(default_factory=list)
    batches: list = field(default_factory=list)
    trashed: list = field(default_factory=list)


@pytest.fixture
def fake_product_media(monkeypatch):
    fake = FakeProductMedia()

    async def fake_upload_images_batch(
        self,
        *,
        images_resource,
        folder,
    ):
        results = []

        for image in images_resource:
            result = type(
                "FakeUploadedImage",
                (),
                {
                    "public_id": f"test/{uuid4()}",
                    "url": "https://example.test/product.jpg",
                },
            )()

            results.append(result)

        fake.uploads.extend(results)
        return results

    async def fake_create_image_batch(
        self,
        *,
        uploads,
        owner_id,
        owner_type,
    ):
        fake.batches.append({
            "uploads": uploads,
            "owner_id": owner_id,
            "owner_type": owner_type,
        })
        return []

    async def fake_move_images_to_trash(
        self,
        *,
        images_public_id,
    ):
        fake.trashed.extend(images_public_id)

    monkeypatch.setattr(
        MediaService,
        "upload_images_batch",
        fake_upload_images_batch,
    )

    monkeypatch.setattr(
        MediaService,
        "create_image_batch",
        fake_create_image_batch,
    )

    monkeypatch.setattr(
        MediaService,
        "move_images_to_trash",
        fake_move_images_to_trash,
    )

    return fake


@pytest.fixture
def fake_product_media_delete(
    monkeypatch,
    fake_product_media,
):
    calls = {
        "delete_images": [],
        "move_images_to_trash": [],
        "recover_images_from_trash": [],
    }

    async def fake_delete_images(
        self,
        *,
        owner_type,
        images_public_id,
    ):
        calls["delete_images"].append({
            "owner_type": owner_type,
            "images_public_id": list(images_public_id),
        })

    async def fake_move_images_to_trash(
        self,
        *,
        images_public_id,
    ):
        calls["move_images_to_trash"].append(
            list(images_public_id)
        )

    async def fake_recover_images_from_trash(
        self,
        *,
        images_public_id,
    ):
        calls["recover_images_from_trash"].append(
            list(images_public_id)
        )

    monkeypatch.setattr(
        MediaService,
        "delete_images",
        fake_delete_images,
    )

    monkeypatch.setattr(
        MediaService,
        "move_images_to_trash",
        fake_move_images_to_trash,
    )

    monkeypatch.setattr(
        MediaService,
        "recover_images_from_trash",
        fake_recover_images_from_trash,
    )

    return calls


@pytest.fixture
def fake_product_cache(monkeypatch):
    invalidations = {
        "entities": [],
        "entity": [],
    }

    async def fake_invalidate_entities(self, tag):
        invalidations["entities"].append(tag)

    async def fake_invalidate_entity(self, tag, entity_id):
        invalidations["entity"].append((tag, entity_id))

    monkeypatch.setattr(
        RedisService,
        "invalidate_entities",
        fake_invalidate_entities,
    )

    monkeypatch.setattr(
        RedisService,
        "invalidate_entity",
        fake_invalidate_entity,
    )

    return invalidations
