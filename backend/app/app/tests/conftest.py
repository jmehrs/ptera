from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="session")
def celery() -> Generator:
    yield celery_app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
