import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from speedapi.app import app
from speedapi.database import get_session
from speedapi.models import metadata_registry


@pytest.fixture
def engine():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    metadata_registry.metadata.create_all(bind=engine)

    yield engine

    metadata_registry.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine):
    with Session(bind=engine) as session:
        yield session


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app=app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_template():
    user_template = {
        'username': 'test_user',
        'email': 'test@email.com',
        'password': 'test_password',
    }

    return user_template


@pytest.fixture
def user(client, user_template):
    response = client.post(
        url='/users/',
        json=user_template,
    )

    return response.json()
