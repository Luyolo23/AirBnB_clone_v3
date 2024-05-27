#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models import storage


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def getAllCities(state_id):
    """Retrieves list of all cities for a given state"""
    city_list = []
    get_state = storage.get("State", state_id)
    if get_state is None:
        abort(404, description="State not found")

    all_cities = {
            k: v
            for k, v in storage.all("City").items() if v.state_id == state_id}
    for city in all_cities.values():
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def getCity(city_id):
    """Retrieve a specific city by ID"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="City not found")
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def DEL_city(city_id):
    """Delete a specific city by ID"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="City not found")

    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def POST_city(state_id):
    """Add a new city to a specific state"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    state = storage.get("State", state_id)
    if state is None:
        abort(404, description="State not found")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def PUT_city(city_id):
    """Update a specific city by ID"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="City not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
