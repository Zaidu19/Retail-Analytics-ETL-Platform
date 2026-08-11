pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.auth",
    "tests.fixtures.customers",
    "tests.fixtures.categories",
    "tests.fixtures.products",
    "tests.fixtures.orders",
    "tests.fixtures.payments",
    "tests.fixtures.refunds",
    "tests.fixtures.inventory_logs",
]

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.database import get_db
from src.db.base import Base
from src.db import models

from src.core.config import settings


TEST_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.TEST_POSTGRES_DB}"
)

test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def db():

    connection = test_engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()

    transaction.rollback()

    connection.close()

@pytest.fixture()
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear() 





