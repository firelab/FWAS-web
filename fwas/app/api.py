from flask import Blueprint, jsonify, make_response

blueprint = Blueprint("api_blueprint", __name__)


@blueprint.route("/ok")
def ok():
    return make_response(jsonify(message="ok"), 200)
