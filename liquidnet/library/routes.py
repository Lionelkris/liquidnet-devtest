from flask import Blueprint, jsonify, request, current_app
from liquidnet.library import library_service
from liquidnet.library.serializer import RequestValidationSchema
from marshmallow import ValidationError

library = Blueprint('library', __name__)


@library.route('/')
def hello():
    return jsonify({"message":"Hello from Library!"}), 200


@library.route('/request', methods=['GET', 'POST'])
def create_request():
    if request.method == "GET":
        results = library_service.list_all_request()
        return jsonify({"requests": results}), 200

    if request.method == "POST":
        data = request.get_json()
        try:
            RequestValidationSchema().load(data)
            results = library_service.create_request(data)
            return jsonify(results), 201
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400


@library.route('/request/<request_id>', methods=['GET', 'DELETE'])
def get_request_by_id(request_id):
    if request.method == 'GET':
        result = library_service.fetch_request_by_id(request_id)
        if not result:
            return jsonify({"error": "Request by this ID is not found"}), 404
        return jsonify(result), 200

    if request.method == 'DELETE':
        result = library_service.delete_request(request_id)
        if not result:
            return jsonify({"error": "Request by this ID is not found"}), 404
        return jsonify(), 200


