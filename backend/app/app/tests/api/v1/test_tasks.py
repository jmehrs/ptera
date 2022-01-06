import pytest
from fastapi.testclient import TestClient

from app.core.celery_app import celery_tasks
from app.core.config import settings


@pytest.mark.parametrize(
    "skip,limit",
    [
        (0, 2),
        (0, -1),
    ],
)
def test_get_tasks(skip: int, limit: int, client: TestClient) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/tasks/", params={"skip": skip, "limit": limit}
    )

    valid_tasks = sorted(celery_tasks())[skip : skip + limit]

    assert response.status_code == 200
    content = response.json()
    assert content == valid_tasks


# TODO: Make test case for this when the actual endpoint is complete
# def test_get_task_info(client: TestClient) -> None:
#     assert False
