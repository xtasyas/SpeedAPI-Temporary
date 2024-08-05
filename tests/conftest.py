import pytest
from fastapi.testclient import TestClient

from speedapi.app import app


@pytest.fixture
def client():
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def user(client):
    client.post(
        url='/users/',
        json=(
            user := {
                'username': 'test_user',
                'email': 'test@email.com',
                'password': 'test_password',
            }
        ),
    )

    return user


@pytest.fixture
def user_template():
    user = {
        'username': 'test_user',
        'email': 'test@email.com',
        'password': 'test_password',
    }

    return user
