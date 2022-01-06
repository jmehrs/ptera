from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas import TaskSignature
from app.tests.utils.canvas import (bad_malformed_canvas,
                                    bad_unregistered_canvas,
                                    create_random_canvas,
                                    good_bare_minimum_canvas,
                                    good_complex_canvas)


@pytest.mark.parametrize(
    "canvas",
    [
        pytest.param(
            good_bare_minimum_canvas,
        ),
        pytest.param(
            good_complex_canvas,
        ),
        pytest.param(bad_unregistered_canvas, marks=pytest.mark.xfail(strict=True)),
        pytest.param(bad_malformed_canvas, marks=pytest.mark.xfail(strict=True)),
    ],
)
def test_create_canvas(canvas: Dict, client: TestClient) -> None:
    response = client.post(f"{settings.API_V1_STR}/canvas/", json=canvas)

    assert response.status_code == 201
    content = response.json()
    assert "id" in content
    assert content["name"] == canvas["name"]
    assert content["canvas"] == TaskSignature(**canvas["canvas"])


def test_get_canvas(client: TestClient, db: Session) -> None:
    canvas = create_random_canvas(db)
    response = client.get(f"{settings.API_V1_STR}/canvas/{canvas.name}")

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == canvas.name
    assert content["id"] == canvas.id
    assert content["canvas"] == TaskSignature(**canvas.canvas)


def test_get_all_canvases(client: TestClient, db: Session) -> None:
    canvases = [create_random_canvas(db) for _ in range(10)]
    skip, limit = 0, len(canvases)

    response = client.get(
        f"{settings.API_V1_STR}/canvas/", params={"skip": skip, "limit": limit}
    )

    assert response.status_code == 200
    content = response.json()
    assert len(canvases) == len(content)


def test_delete_canvas(client: TestClient, db: Session) -> None:
    canvas = create_random_canvas(db)
    response_deleted = client.delete(f"{settings.API_V1_STR}/canvas/{canvas.name}")
    response_invalid = client.get(f"{settings.API_V1_STR}/canvas/{canvas.name}")

    assert response_invalid.status_code == 404

    assert response_deleted.status_code == 200
    content = response_deleted.json()
    assert content["name"] == canvas.name
    assert content["id"] == canvas.id
    assert content["canvas"] == TaskSignature(**canvas.canvas)
