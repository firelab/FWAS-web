from flask import Blueprint, current_app, g
from flask_apispec import marshal_with, use_kwargs

from .. import queries, serialize
from ..database import db
from ..extensions import bcrypt
from ..models import BlacklistToken, User
from .utils import jwt_login_required

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/register", methods=["POST"])
@use_kwargs(serialize.NewUserParameter)
@marshal_with(serialize.LoginResult)
def create_user(**kwargs):
    email = kwargs["email"]
    if queries.get_user_by_email(email):
        response = {
            "status": "fail",
            "message": f"User {email} already exists. Please log in.",
        }
        return response, 202

    try:
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()

        auth_token = User.generate_auth_token(user.id)
        response = {
            "status": "success",
            "message": "Successfully registered.",
            "auth_token": auth_token.decode(),
        }
        return response, 201
    except Exception as exc:
        current_app.logger.exception(exc)
        response = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return response, 500


@auth_blueprint.route("/login", methods=["POST"])
@use_kwargs(serialize.LoginParameter)
@marshal_with(serialize.LoginResult)
def user_login(**kwargs):
    try:
        email = kwargs["email"]
        password = kwargs["password"]
        user = queries.get_user_by_email(email)

        if not user or not bcrypt.check_password_hash(user.password, password):
            response = {
                "status": "fail",
                "message": "User does not exist or password is invalid.",
            }
            return response, 404

        auth_token = User.generate_auth_token(user.id)
        response = {
            "status": "success",
            "message": "Successfully logged in.",
            "auth_token": auth_token.decode(),
        }
        return response, 200
    except Exception as e:
        current_app.logger.exception(e)
        response = {"status": "fail", "message": "Try again."}
        return response, 500


@auth_blueprint.route("/status", methods=["GET"])
@marshal_with(serialize.LoginStatusResult, code=200)
@jwt_login_required
def user_status():
    response = {
        "status": "success",
        "data": {
            "user_id": g.user.id,
            "email": g.user.email,
            "created_at": g.user.created_at,
        },
    }

    return response, 200


@auth_blueprint.route("/logout", methods=["POST"])
@marshal_with(serialize.LoginResult, code=200)
@marshal_with(serialize.LoginResult, code=500)
@jwt_login_required
def user_logout():
    auth_token = g.auth_token
    blacklist_token = BlacklistToken(token=auth_token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        response = {"status": "success", "message": "Successfully logged out."}
        return response, 200
    except Exception:
        current_app.logger.exception("/logout exception caught")
        response = {
            "status": "fail",
            "message": "Log out failed. Please try again or contact support.",
        }
        return response, 500
