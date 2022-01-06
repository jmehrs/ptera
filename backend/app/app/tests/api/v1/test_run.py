from typing import Dict

import pytest
from app.core.config import settings
from app.tests.utils.canvas import create_test_canvas
from app.tests.utils.task import (
    bad_malformed_task,
    bad_unregistered_task,
    good_bare_minimum_task,
    good_complex_task,
)
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    "canvas",
    [
        pytest.param(good_bare_minimum_task),
        pytest.param(good_complex_task),
        pytest.param(bad_unregistered_task, marks=pytest.mark.xfail(strict=True)),
        pytest.param(bad_malformed_task, marks=pytest.mark.xfail(strict=True)),
    ],
)
def test_run_unnamed_canvas(canvas: Dict, client: TestClient) -> None:
    response = client.post(f"{settings.API_V1_STR}/run/", json=canvas)

    assert response.status_code == 201
    content = response.json()
    assert "id" in content


@pytest.mark.parametrize(
    "canvas_exists",
    [pytest.param(True), pytest.param(False, marks=pytest.mark.xfail(strict=True))],
)
def test_run_named_canvas(canvas_exists: bool, client: TestClient, db: Session) -> None:
    canvas_name = (
        create_test_canvas(db).name if canvas_exists else "Non-existant Canvas"
    )
    response = client.post(f"{settings.API_V1_STR}/run/{canvas_name}")

    assert response.status_code == 201
    content = response.json()
    assert "id" in content
