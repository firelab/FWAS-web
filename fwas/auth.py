import jwt
import bcrypt
from fwas import config, utils


def encrypt_password(plaintext_password: str) -> str:
    if plaintext_password:
        password = bcrypt.generate_password_hash(
            plaintext_password, config.BCRYPT_LOG_ROUNDS
        ).decode()
        return password

    return None


def get_auth_token(user_id):
    expiration = config.REMEMBER_COOKIE_DURATION.total_seconds()
    return generate_auth_token(user_id, expiration=expiration)


def verify_auth_token(auth_token):
    """
    Verify the auth token by returning the user assocaiated
    """
    try:
        payload = jwt.decode(auth_token, config.SECRET_KEY, algorithms="HS256")
        user_id = payload["sub"]
    except jwt.ExpiredSignatureError:
        return None  # 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return None  # 'Invalid token. Please log in again.'

    user = User.query.get(user_id)
    return user


def generate_auth_token(user_id, expiration: int = 3600) -> str:
    payload = {
        "exp": utils.get_current_utc_datetime() + timedelta(days=0, seconds=expiration),
        "iat": utils.get_current_utc_datetime(),
        "sub": user_id,
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")


def authenticated(self, with_password=True, password=""):
    """
    Ensure a user is authenticated, and optionally check their password.
    """
    if with_password:
        return bcrypt.check_password_hash(self.password, password)

    return True
