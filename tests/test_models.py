from fwas import db
from fwas.models import User


def test_encode_auth_token(app):
    user = User(
        email='test@test.com',
        password='test'
    )
    db.session.add(user)
    db.session.commit()
    auth_token = User.generate_auth_token(user.id)
    assert isinstance(auth_token, bytes)

def test_verify_auth_token(app):
    user = User(
        email='test@test.com',
        password='test'
    )
    db.session.add(user)
    db.session.commit()
    auth_token = User.generate_auth_token(user.id)
    decoded_user = User.verify_auth_token(auth_token)

    assert isinstance(auth_token, bytes)
    assert decoded_user == user
    assert decoded_user.id == 1
