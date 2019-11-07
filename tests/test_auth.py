import json
import pytest

from fwas.models import User
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
