import pytest


def test_api_ok(app):
    response = app.get('/api/ok')

    assert response.status_code == 200
    assert response.json == {'message': 'ok'}
