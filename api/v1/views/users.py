#!/usr/bin/python3
"""
users.py
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getAllUsers():
    """Retrieves the list of all User objects"""
    user_list = [user.to_dict() for user in storage.all('User').values()]
    return jsonify(user_list)


@app_views.route(
        '/users/<user_id>', strict_slashes=False, methods=['GET'])
def GET_user(user_id):
    """Retrieves a specific User object by ID"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def DEL_user(user_id):
    """Deletes a specific User object by ID"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404, description="User not found")

    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def POST_user():
    """Creates a new User object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    required_fields = ['email', 'password']

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    new_user = User(**data)
    storage.new(new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PUT_user(user_id):
    """Updates a specific User object by ID"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404, description="User not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "created_at", "updated_at", "email"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
