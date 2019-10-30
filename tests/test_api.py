import pytest


def test_api_ok(client):
    response = client.get('/api/ok')

    assert response.status_code == 200
    assert response.json == {'message': 'ok'}


# TODO (lmalott): Test user creation outside of US
# TODO (lmalott): Test alert creation outside of US
# TODO (lmalott): Test succesful user creation
# TODO (lmalott): Test user already exists
