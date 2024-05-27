#!/usr/bin/python3
"""
states.py
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getAllStates():
    """Retrieves the list of all State objects"""
    all_states = [item.to_dict() for item in storage.all('State').values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def GET_state(state_id):
    """GET State object, else raise 404"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def DEL_state(state_id):
    """Delete a state object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_state():
    """Adds state, raises 400 if not valid JSON or missing name"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    storage.close()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def PUT_state(state_id):
    """Updates a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "created_at", "updated_at"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()
    storage.close()
    return jsonify(state.to_dict()), 200
