#!/usr/bin/python3
"""
New view for Place objects that handles all default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models.city import City
from models import storage


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def getAllPlaces(city_id):
    """Retrieves all Place objects of a City"""
    place_list = [place.to_dict() for place in storage.all(
        'Place').values() if place.city_id == city_id]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def getPlace(place_id):
    """Retrieves a specific Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404, description="Place not found")
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def DEL_place(place_id):
    """Deletes a specific Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404, description="Place not found")

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def POST_place(city_id):
    """Creates a new Place object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    required_fields = ['name', 'user_id']

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404, description="User not found")

    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="City not found")

    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
        '/places/<place_id>', methods=['PUT'], strict_slashes=False)
def PUT_place(place_id):
    """Updates a specific Place object by ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404, description="Place not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "city_id", "user_id", "created_at", "updated_at"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
