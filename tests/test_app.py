from http import HTTPStatus

from speedapi.schemas import UserPublic


def test_app(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to SpeedAPI!'}


def test_create_users(client, user_template):
    response = client.post(url='/users/', json=user_template)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == UserPublic(id=1, **user_template).model_dump()


def test_create_user_that_already_exists(client, user, user_template):
    response = client.post(url='/users/', json=user_template)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User already exists.'}


def test_read_users_without_users_registered(client):
    response = client.get(url='/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_one_user(client, user):
    response = client.get(url='/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user]}


def test_update_users(client, user, user_template):
    user_template['username'] = 'new_test_username'
    response = client.put(url='/users/1', json=user_template)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_template


def test_update_user_that_not_exists(client, user_template):
    response = client.put(url='/users/0', json=user_template)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not exists.'}


def test_delete_user(client, user):
    response = client.delete(url='/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User with ID 1 has been deleted.'}


def test_delete_user_that_not_exists(client):
    response = client.delete(url='/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not exists.'}
