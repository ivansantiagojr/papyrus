from src.users.schemas import UserPublic


def test_create_user_admin(client, admin_user, admin_token):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'username': 'alice', 'password': '12345', 'role': 'WRITER'},
    )

    assert response.status_code == 201
    assert response.json() == {'username': 'alice', 'role': 'WRITER', 'id': 5}


def test_create_user_username_already_exists_admin(
    client, user, admin_user, admin_token
):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'username': user.username, 'password': 'test', 'role': 'WRITER'},
    )

    assert response.status_code == 400


def test_create_user_non_admin(client, user, token):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'alice', 'password': '12345', 'role': 'WRITER'},
    )

    assert response.status_code == 403


def test_get_users_admin(client, admin_user, admin_token):
    user_schema = UserPublic.model_validate(admin_user).model_dump()
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {admin_token}'},
    )
    assert response.json() == [user_schema]


def test_get_users_not_admin(client, user, token):
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 403


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'password': 'secret',
            'role': 'WRITER',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'alice',
        'role': 'WRITER',
        'id': user.id,
    }


def test_update_non_existing_user_non_admin(client, token):
    response = client.put(
        '/users/100',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'password': 'secret',
            'role': 'ADMIN',
        },
    )

    assert response.status_code == 403


def test_update_non_existing_user_admin(client, admin_user, admin_token):
    response = client.put(
        '/users/100',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'username': 'alice',
            'password': 'secret',
            'role': 'ADMIN',
        },
    )

    assert response.status_code == 404


def test_update_user_to_admin_from_admin(
    client, user, admin_user, admin_token
):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'username': 'alice',
            'password': 'secret',
            'role': 'ADMIN',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'alice',
        'role': 'ADMIN',
        'id': user.id,
    }


def test_delete_user_non_admin(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_delete_user_wrong_user_non_admin(client, user, user2, token):
    response = client.delete(
        f'/users/{user2.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not allowed'}


def test_delete_non_existing_user_admin(client, admin_token):
    response = client.delete(
        '/users/100',
        headers={'Authorization': f'Bearer {admin_token}'},
    )
    assert response.status_code == 404
