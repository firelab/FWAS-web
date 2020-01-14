import json

import arrow
import pytest
from freezegun import freeze_time


def register_user(client, email, password):
    response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password,
            phone='12345678910'
        )),
        content_type='application/json'
    )
    return response


def create_alert(client, auth_token):
    alert = {
        'name': 'Test Alert',
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


def test_user_details(client):
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
        'active': True,
        'alerts': [],
        'notifications': [],
        'subscriptions': [],
        'phone': '12345678910',
        'sign_in_count': 0,
        'role': 'member',
        'current_sign_in_at': None,
        'current_sign_in_ip': None,
        'last_sign_in_at': None,
        'last_sign_in_ip': None
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
        'name': 'Test Alert',
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


def test_alert_details_filter(client):
    with freeze_time("2019-11-01 12:00:00"):
        response = register_user(client, 'test@test.com', '12345678910')
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'

    auth_token = data['auth_token']

    with freeze_time("2019-11-01 12:00:00"):
        response = create_alert(client, auth_token)
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'

    with freeze_time("2019-11-01 12:09:00"):
        response = create_alert(client, auth_token)
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'

    with freeze_time("2019-11-01 12:09:00"):
        response = client.get('/api/alerts',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
    alerts = response.json

    assert response.status_code == 200
    assert len(alerts) == 2

    for i, alert in enumerate(alerts):
        assert alert['id'] == i + 1
        assert alert['longitude'] == -90.1854
        assert alert['latitude'] == 38.6247
        assert alert['radius'] == 20000.0
        assert alert['check_thunderstorms'] == False
        assert alert['precipitation_limit'] == 5.0
        assert alert['relative_humidity_limit'] == 80.0
        assert alert['temperature_limit'] == 0.0
        assert alert['wind_limit'] == 1.0
        assert alert['timezone'] == 'America/Chicago'

    # freeze_time unfortunately does not work with the database model
    # timestamps. Going to shave off a microsecond from the latest alert
    # to confirm filtering based on timestamps works.
    timestamp = arrow.get(alerts[1]['created_at']).shift(microseconds=-1).isoformat().replace('+00:00', 'Z')
    # Confirm only one alert is returned if we specify the 'since'
    # parameter
    with freeze_time("2019-11-01 12:09:00"):
        response = client.get(
            f'/api/alerts?since={timestamp}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
    data = response.json
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == 2

    # Confirm that providing a timestamp greater than all the alert created_at
    # times returns an empty list
    timestamp = arrow.get(alerts[1]['created_at']).shift(microseconds=1).isoformat().replace('+00:00', 'Z')
    with freeze_time("2019-11-01 12:09:00"):
        response = client.get(
            f'/api/alerts?since={timestamp}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
    data = response.json
    assert response.status_code == 200
    assert len(data) == 0


def test_alert_subscribe(client):
    response = register_user(client, 'test@test.com', '12345678910')
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'

    response = register_user(client, 'subscriber@test.com', '12345678910')
    subscriber_data = response.json
    assert response.status_code == 201
    assert subscriber_data['status'] == 'success'

    auth_token = data['auth_token']

    response = create_alert(client, auth_token)
    data = response.json
    assert response.status_code == 201
    assert data['status'] == 'success'

    alert_uuid = data['alert_uuid']
    subscriber_auth_token = subscriber_data['auth_token']

    response = client.put(
        f'/api/alerts/subscribe/{alert_uuid}',
        headers=dict(
            Authorization='Bearer ' + subscriber_auth_token
        )
    )
    data = response.json
    expected = {
        "status": "success",
        "message": "Successfully subscribed to alert."
    }

    assert response.status_code == 200
    assert data == expected

