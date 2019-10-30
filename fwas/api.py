from flask import Blueprint, g, jsonify, make_response
from flask_apispec import marshal_with, use_kwargs
from flask_httpauth import HTTPBasicAuth

from . import models, queries, serialize
from .database import db

auth = HTTPBasicAuth()
blueprint = Blueprint("api_blueprint", __name__)


@blueprint.route("/ok")
def ok():
    return make_response(jsonify(message="ok"), 200)


@blueprint.route("/token")
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})


@blueprint.route("/user/<int:user_id>")
@marshal_with(serialize.UserSchema, code=200)
@marshal_with(serialize.UserError, code=400)
def user(user_id):
    """User detail view."""
    # TODO (lmalott): Add auth mechanism for clients to access
    user = queries.get_user(user_id)
    if not user:
        return {"message": f"User {user_id} does not exist."}, 400

    return user, 200


@blueprint.route("/user", methods=["POST"])
@use_kwargs(serialize.NewUserParameter)
@marshal_with(serialize.NewUserResult, code=201)
def create_user(**kwargs):
    email = kwargs["email"]
    if queries.get_user_by_email(email):
        return {"message": f"User {email} already exists."}, 400

    user = models.User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user, 201


@blueprint.route("/user/<int:user_id>/alerts")
@marshal_with(serialize.AlertSchema(many=True), code=200)
def user_alerts(user_id):
    alerts = queries.get_user_alerts(user_id)

    return alerts, 200


@blueprint.route("/user/<int:user_id>/notifications")
@marshal_with(serialize.NotificationSchema(many=True), code=200)
def user_notifications(user_id):
    notifications = queries.get_user_notifications(user_id)

    return notifications, 200


@blueprint.route("/notification/<id>")
def notification():
    pass


@blueprint.route("/alert/<id>")
def alert():
    pass
