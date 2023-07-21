from src.users.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users',
        json={'username': 'alice', 'password': '12345', 'role': 'WRITER'},
    )

    assert response.status_code == 201
    assert response.json() == {'username': 'alice', 'role': 'WRITER', 'id': 1}


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={'username': 'test', 'password': 'test', 'role': 'WRITER'},
    )

    assert response.status_code == 400


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == []


def test_get_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == [user_schema]


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'password': 'secret',
            'role': 'ADMIN',
        },
    )

    assert response.status_code == 200
    assert response.json() == {'username': 'alice', 'role': 'ADMIN', 'id': 1}


def test_update_non_existing_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'password': 'secret',
            'role': 'ADMIN',
        },
    )

    assert response.status_code == 404


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_delete_non_existing_user(client):
    response = client.delete('/users/1')
    assert response.status_code == 404
