import pytest
from app.core.config import settings
from app.tests.utils.celery import run_task
from celery import Celery
from fastapi.testclient import TestClient


def test_get_result(celery: Celery, client: TestClient) -> None:
    result = run_task(celery)
    result.get()  # Block until task is done
    response = client.get(f"{settings.API_V1_STR}/result/{result.id}")

    assert response.status_code == 200
    content = response.json()
    assert content == "pong"


def test_get_pending_result(celery: Celery, client: TestClient) -> None:
    result = run_task(celery, countdown=1)
    response = client.get(f"{settings.API_V1_STR}/result/{result.id}")

    assert response.status_code == 202
    content = response.json()
    assert "detail" in content


@pytest.mark.skip(
    "Ability to check for all task_ids in backend has not been implemented yet"
)
def test_get_nonexistant_result() -> None:
    # TODO: Find way to check backend for all task_id's
    pass
