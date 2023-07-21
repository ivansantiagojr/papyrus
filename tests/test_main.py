def test_root_must_return_200_and_ok(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'ok'}
