from flask import Blueprint, current_app, g, jsonify, make_response
from flask_apispec import marshal_with, use_kwargs
from geoalchemy2.elements import WKTElement

from . import models, queries, serialize
from .auth.utils import login_required
from .database import db

blueprint = Blueprint("api_blueprint", __name__)


@blueprint.route("/ok")
def ok():
    return make_response(jsonify(message="ok"), 200)


@blueprint.route("/token")
@login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})


@blueprint.route("/me", methods=["GET"])
@marshal_with(serialize.UserSchema, code=200)
@marshal_with(serialize.UserError, code=400)
@login_required
def user():
    user = g.user
    if not user:
        return {"message": f"User {user.id} does not exist."}, 400

    return user, 200


@blueprint.route("/alerts", methods=["GET"])
@use_kwargs(serialize.AlertDetailsParameters)
@marshal_with(serialize.AlertSchema(many=True), code=200)
@login_required
def user_alerts(**kwargs):
    since = kwargs.get("since")
    user_id = g.user.id
    alerts = queries.get_user_alerts(user_id, since).all()

    return alerts, 200


@blueprint.route("/alerts", methods=["POST"])
@use_kwargs(serialize.NewAlertSchema)
@marshal_with(serialize.AlertCreationSuccess, code=201)
@marshal_with(serialize.RequestError, code=400)
@marshal_with(serialize.InternalError, code=500)
@login_required
def create_alert(**kwargs):
    user = g.user
    data = kwargs
    errors = serialize.new_alert_schema.validate(data)
    if errors:
        current_app.logger.warning(f"Serialization failures: {errors}")
        response = {"status": "fail", "message": str(errors)}
        return response, 400

    try:
        pt = WKTElement(f"POINT({data['longitude']} {data['latitude']})", srid=4326)
        alert = models.Alert(user_id=user.id, expires_in_hours=6.0, geom=pt, **kwargs)
        db.session.add(alert)
        db.session.commit()

        response = {
            "status": "success",
            "message": "Successfully created alert",
            "alert_id": alert.id,
        }

        return response, 201
    except Exception:
        current_app.logger.exception("Failed to create alert.")
        response = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return response, 500


@blueprint.route("/notifications", methods=["GET"])
@marshal_with(serialize.NotificationSchema(many=True), code=200)
@login_required
def user_notifications(user_id):
    # TODO (lmalott): add query param to filter based on age of notification
    notifications = queries.get_user_notifications(user_id)

    return notifications, 200
