import json
import pytest



def register_user(client, email, password):
    response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password,
            phone='123456'
        )),
        content_type='application/json'
    )
    return response


def create_alert(client, auth_token):
    alert = {
        'latitude': 38.6247,
        'longitude': -90.1854,
        'radius': 20000,
        'timezone': "America/Chicago",
        'temperature_limit': 0.0,  # celcius
        'precipitation_limit': 5.0,  # inches
        'relative_humidity_limit': 80.0,  # percent
        'wind_limit': 1.0,  # meters / second
    }
    response = client.post(
        '/api/alerts',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=alert
    )
    return response


def test_api_ok(client):
    response = client.get('/api/ok')

    assert response.status_code == 200
    assert response.json == {'message': 'ok'}


def test_user_details(client, freezer):
    response = register_user(client, 'test@test.com', '12345678910')
    data = response.json

    assert response.status_code == 201
    assert data['status'] == 'success'

    response = client.get(
        '/api/me',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        )
    )

    data = response.json
    expected = {
        'id': 1,
        'email': 'test@test.com',
        'admin': False,
        'alerts': [],
        'notifications': [],
        'phone': '123456'
    }
    assert expected.items() < data.items()


def test_user_details_without_logging_in(client):
    response = client.get('/api/me')
    data = response.json

    assert response.status_code == 403
    assert data['status'] == 'fail'
    assert data['message'] == 'Provide a valid auth token.'


def test_alert_create(client):
    response = register_user(client, 'test@test.com', '12345678910')
    data = response.json

    assert response.status_code == 201
    assert data['status'] == 'success'

    alert = {
        'latitude': 38.6247,
        'longitude': -90.1854,
        'radius': 20000,
        'timezone': "America/Chicago",
        'temperature_limit': 0.0,  # celcius
        'precipitation_limit': 5.0,  # inches
        'relative_humidity_limit': 80.0,  # percent
        'wind_limit': 1.0,  # meters / second
    }
    response = client.post(
        '/api/alerts',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        data=alert
    )
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully created alert'
    assert data['alert_id'] == 1


def test_alert_create_bad_input(client):
    response = register_user(client, 'test@test.com', '12345678910')
    data = response.json

    assert response.status_code == 201
    assert data['status'] == 'success'

    alert = {
        'latitude': 38.6247,
        'longitude': -90.1854,
        'timezone': "America/Chicago",
        'temperature_limit': 0.0,  # celcius
        'precipitation_limit': 5.0,  # inches
        'relative_humidity_limit': 80.0,  # percent
        'wind_limit': 1.0,  # meters / second
    }
    response = client.post(
        '/api/alerts',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        data=alert
    )
    assert response.status_code == 422


def test_alert_details(client):
    response = register_user(client, 'test@test.com', '12345678910')
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'

    auth_token = data['auth_token']

    response = create_alert(client, auth_token)
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'


    response = client.get('/api/alerts',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    data = response.json

    assert response.status_code == 200
    assert len(data) == 1

    alert = data[0]
    assert alert['id'] == 1
    assert alert['longitude'] == -90.1854
    assert alert['latitude'] == 38.6247
    assert alert['radius'] == 20000.0
    assert alert['check_thunderstorms'] == False
    assert alert['precipitation_limit'] == 5.0
    assert alert['relative_humidity_limit'] == 80.0
    assert alert['temperature_limit'] == 0.0
    assert alert['wind_limit'] == 1.0
    assert alert['timezone'] == 'America/Chicago'
