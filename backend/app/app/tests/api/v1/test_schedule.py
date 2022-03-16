from typing import Dict

import pytest
from app.core.config import settings
from app.tests.utils.canvas import good_bare_minimum_canvas
from app.tests.utils.crontab_schedule import random_crontab_schedule_schema
from app.tests.utils.interval_schedule import random_interval_schedule_schema
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# @pytest.mark.parametrize(
#     "canvas",
#     [
#         pytest.param(
#             good_bare_minimum_canvas,
#         ),
#         pytest.param(
#             good_complex_canvas,
#         ),
#         pytest.param(bad_unregistered_canvas, marks=pytest.mark.xfail(strict=True)),
#         pytest.param(bad_malformed_canvas, marks=pytest.mark.xfail(strict=True)),
#     ],
# )
def test_create_schedule(schedule: Dict, client: TestClient) -> None:
    response = client.post(f"{settings.API_V1_STR}/schedule/", json=schedule)

    assert response.status_code == 201
    content = response.json()
    assert "id" in content
    assert content["name"] == schedule["name"]
    # assert content["schedule"] == TaskSignature(**schedule["schedule"])


# def test_get_schedule(client: TestClient, db: Session) -> None:
#     schedule = create_random_schedule(db)
#     response = client.get(f"{settings.API_V1_STR}/schedule/{schedule.name}")

#     assert response.status_code == 200
#     content = response.json()
#     assert content["name"] == schedule.name
#     assert content["id"] == schedule.id
#     assert content["schedule"] == TaskSignature(**schedule.schedule)


# def test_get_all_schedules(client: TestClient, db: Session) -> None:
#     schedules = [create_random_schedule(db) for _ in range(10)]
#     skip, limit = 0, len(schedules)

#     response = client.get(
#         f"{settings.API_V1_STR}/schedule/", params={"skip": skip, "limit": limit}
#     )

#     assert response.status_code == 200
#     content = response.json()
#     assert len(schedules) == len(content)


# def test_delete_schedule(client: TestClient, db: Session) -> None:
#     schedule = create_random_schedule(db)
#     response_deleted = client.delete(f"{settings.API_V1_STR}/schedule/{schedule.name}")
#     response_invalid = client.get(f"{settings.API_V1_STR}/schedule/{schedule.name}")

#     assert response_invalid.status_code == 404

#     assert response_deleted.status_code == 200
#     content = response_deleted.json()
#     assert content["name"] == schedule.name
#     assert content["id"] == schedule.id
#     assert content["schedule"] == TaskSignature(**schedule.canvas)
