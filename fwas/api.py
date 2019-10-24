from flask import Blueprint, jsonify, make_response

from .database import conn

blueprint = Blueprint("api_blueprint", __name__)


@blueprint.route("/ok")
def ok():
    return make_response(jsonify(message="ok"), 200)


@blueprint.route("/user/<int:user_id>")
def user(user_id):
    # TODO (lmalott): Add auth mechanism for clients to access
    # TODO (lmalott): Add input validation checking
    row = conn.query(
        "select * from public.user where id=:user_id", user_id=user_id
    ).first(as_dict=True)

    return jsonify(row), 400


@blueprint.route("/user/<int:user_id>/alerts")
def user_alerts(user_id):
    alerts = conn.query(
        "select * from alert where user_id=:user_id", user_id=user_id
    ).all(as_dict=True)

    return jsonify(alerts), 400


@blueprint.route("/user/<int:user_id>/notifications")
def user_notifications(user_id):
    notifications = conn.query(
        "select * from notification where user_id=:user_id", user_id=user_id
    ).all(as_dict=True)

    return jsonify(notifications), 400


@blueprint.route("/notification/<id>")
def notification():
    pass


@blueprint.route("/alert/<id>")
def alert():
    pass
