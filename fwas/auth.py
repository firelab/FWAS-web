import jwt
import bcrypt
from loguru import logger
from datetime import timedelta

from fwas import config, utils

from fwas.crud import get_user


def encrypt_password(plaintext_password: str) -> str:
    if plaintext_password:
        salt = bcrypt.gensalt(config.BCRYPT_LOG_ROUNDS)
        password = bcrypt.hashpw(plaintext_password.encode('utf-8'), salt).decode()
        return password

    return None


def get_user_id_from_token(auth_token):
    """
    Verify the auth token by returning the user assocaiated
    """
    try:
        payload = jwt.decode(auth_token, config.SECRET_KEY, algorithms="HS256")
        user_id = payload["sub"]
    except jwt.ExpiredSignatureError:
        logger.info('Expired signature from token')
        return None  # 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        logger.info('Received invalid token.')
        return None  # 'Invalid token. Please log in again.'

    return user_id


def get_auth_token(user_id):
    expiration = config.REMEMBER_COOKIE_DURATION
    return generate_auth_token(user_id, expiration=expiration)


def generate_auth_token(user_id, expiration: int = 3600) -> str:
    payload = {
        "exp": utils.get_current_utc_datetime() + timedelta(days=0, seconds=expiration),
        "iat": utils.get_current_utc_datetime(),
        "sub": user_id,
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")


def authenticated(user_password, with_password=True, password=""):
    """
    Ensure a user is authenticated, and optionally check their password.
    """
    if with_password:
        return bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8'))

    return True
