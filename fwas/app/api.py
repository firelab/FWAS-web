from flask import Blueprint, make_response, jsonify

blueprint = Blueprint('api_blueprint', __name__)



@blueprint.route('/ok')
def ok():
    return make_response(jsonify(message='ok'), 200)
