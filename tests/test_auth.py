import json
import pytest
from freezegun import freeze_time

from fwas.models import User, BlacklistToken
from fwas.database import db


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
    data = json.loads(response.data.decode())
    return response, data


def login_user(client, email, password):
    response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    return response, data


def test_registration(client):
    response, data = register_user(client, 'test@test.com', '12345678910')
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully registered.'
    assert data['auth_token']
    assert response.content_type == 'application/json'
    assert response.status_code == 201


def test_registered_with_already_registered_user(client):
    user = User(
        email='test@test.com',
        password='test1234566'
    )
    db.session.add(user)
    db.session.commit()

    response, data = register_user(client, 'test@test.com', '12345678910')
    assert data['status'] == 'fail'
    assert data['message'] == 'User test@test.com already exists. Please log in.'
    assert response.content_type == 'application/json'
    assert response.status_code, 202


def test_registered_user_login(client):
    resp_register, data_register = register_user(client, 'test@test.com', '12345678910')
    assert data_register['status'] == 'success'
    assert data_register['message'] == 'Successfully registered.'
    assert data_register['auth_token']
    assert resp_register.content_type == 'application/json'
    assert resp_register.status_code == 201

    response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='test@test.com',
            password='12345678910'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['message'] == 'Successfully logged in.'
    assert data['status'] == 'success'
    assert data['auth_token']
    assert response.content_type == 'application/json'
    assert response.status_code == 200


def test_non_registered_user_login(client):
    response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='test@test.com',
            password='12345678910'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'fail'
    assert data['message'] == 'User does not exist or password is invalid.'
    assert response.content_type == 'application/json'
    assert response.status_code == 404


def test_user_status(client):
    register_resp, register_data = register_user(client, 'test@test.com', '12345678910')

    response = client.get(
        '/auth/status',
        headers=dict(
            Authorization='Bearer ' + register_data['auth_token']
        )
    )
    data = json.loads(response.data.decode())

    assert data['status'] == 'success'
    assert data['data'] is not None
    assert data['data']['email'] == 'test@test.com'
    assert data['data']['admin'] == False
    assert response.status_code, 200


def test_user_status_invalid_token(client):
    register_resp, register_data = register_user(client, 'test@test.com', '12345678910')

    response = client.get(
        '/auth/status',
        headers=dict(
            Authorization='Bearer ' + register_data['auth_token'] + '123'
        )
    )
    data = json.loads(response.data.decode())

    assert data['status'] == 'fail'
    assert data['message'] == 'Either the signature expired or token is invalid. Please log in again.'
    assert response.status_code, 401


def test_user_status_expired_token(client):
    user = User(email='test@test.com', password='12345678910')
    db.session.add(user)
    db.session.commit()

    auth_token = User.generate_auth_token(user.id, expiration=-1)

    response = client.get(
        '/auth/status',
        headers=dict(
            Authorization='Bearer ' + auth_token.decode()
        )
    )
    data = json.loads(response.data.decode())

    assert data['status'] == 'fail'
    assert data['message'] == 'Either the signature expired or token is invalid. Please log in again.'
    assert response.status_code, 401


def test_valid_logout(client):
    register_resp, register_data = register_user(client, 'test@test.com', '12345678910')
    assert register_data['status'] == 'success'
    assert register_data['message'] == 'Successfully registered.'
    assert register_data['auth_token']
    assert register_resp.content_type == 'application/json'
    assert register_resp.status_code == 201

    login_resp, login_data = login_user(client, 'test@test.com', '12345678910')
    assert login_data['status'] == 'success'
    assert login_data['message'] == 'Successfully logged in.'
    assert login_data['auth_token']
    assert login_resp.content_type == 'application/json'
    assert login_resp.status_code == 200

    response = client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer ' + json.loads(
                login_resp.data.decode()
            )['auth_token']
        )
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged out.'
    assert response.status_code == 200


def test_invalid_logout_token_expired(client):
        register_resp, register_data = register_user(client, 'test@test.com', '12345678910')
        assert register_data['status'] == 'success'
        assert register_resp.status_code == 201

        with freeze_time("1970-01-01"):
            login_resp, login_data = login_user(client, 'test@test.com', '12345678910')
        assert login_data['status'] == 'success'
        assert login_resp.status_code == 200

        response = client.post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_resp.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        assert data['status'] == 'fail'
        assert data['message'] == 'Either the signature expired or token is invalid. Please log in again.'
        assert response.status_code == 401


def test_valid_blacklisted_token_logout(client):
    # Register and login user to obtain auth token
    register_resp, register_data = register_user(client, 'test@test.com', '12345678910')
    assert register_data['status'] == 'success'
    assert register_resp.status_code == 201

    login_resp, login_data = login_user(client, 'test@test.com', '12345678910')
    assert login_data['status'] == 'success'
    assert login_resp.status_code == 200

    # blacklist the user's valid token
    token = json.loads(login_resp.data.decode())['auth_token']
    blacklist_token = BlacklistToken(token=token)
    db.session.add(blacklist_token)
    db.session.commit()

    response = client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer ' + token
        )
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'fail'
    assert data['message'] == 'Token is blacklisted. Please log in again.'
    assert response.status_code == 401
