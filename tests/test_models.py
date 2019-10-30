from fwas import db
from fwas.models import User


def test_encode_auth_token(app):
    user = User(
        email='test@test.com',
        password='test'
    )
    db.session.add(user)
    db.session.commit()
    auth_token = user.generate_auth_token(user.id)
    assert isinstance(auth_token, bytes)
