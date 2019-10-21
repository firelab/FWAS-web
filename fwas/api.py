from flask import Blueprint, jsonify, make_response

from .database import conn

blueprint = Blueprint("api_blueprint", __name__)


@blueprint.route("/ok")
def ok():
    return make_response(jsonify(message="ok"), 200)


@blueprint.route("/user/<int:user_id>")
def user(user_id):
    # TODO (lmalott): Add input validation checking
    row = conn.query(
        "select * from public.user where :user_id", user_id=user_id
    ).first()

    return jsonify(row.as_dict()), 400


@blueprint.route("/user/<id>/alerts")
def user_alerts():
    pass


@blueprint.route("/notification/<id>")
def notification():
    pass


@blueprint.route("/alert/<id>")
def alert():
    pass
