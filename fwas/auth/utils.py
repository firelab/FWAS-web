from functools import wraps

from flask import g, request
from flask_apispec import marshal_with

from .. import serialize
from ..models import User


def login_required(f):
    @wraps(f)
    @marshal_with(serialize.LoginResult, code=401)
    def wrap(*args, **kwargs):
        # TODO (lmalott): handle user/pass combo as well.
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if not auth_token:
            response = {"status": "fail", "message": "Provide a valid auth token."}
            return response, 401

        user = User.verify_auth_token(auth_token)
        if user is None:
            response = {
                "status": "fail",
                "message": "Either the signature expired or token is invalid. Please log in again.",
            }
            return response, 401

        g.user = user
        return f(*args, **kwargs)

    return wrap


def admin_login_required(f):
    def wrap(*args, **kwargs):
        if not g.user.is_admin:
            return {"message": "Must be admin to view."}, 401
        return f(*args, **kwargs)

    return wrap
