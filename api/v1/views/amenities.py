#!/usr/bin/python3
"""
New view for Amenity objects that handles all default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def ALL_Amenities():
    """Retrieves the list of all Amenity objects"""
    amenity_list = [
            amenity.to_dict() for amenity in storage.all('Amenity').values()]
    return jsonify(amenity_list)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def GET_Amenity(amenity_id):
    """Retrieves a specific Amenity object by ID"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, description="Amenity not found")
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def DEL_Amenity(amenity_id):
    """Deletes a specific Amenity object by ID"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, description="Amenity not found")

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def POST_Amenity():
    """Creates a new Amenity object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def PUT_Amenity(amenity_id):
    """Updates a specific Amenity object by ID"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, description="Amenity not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
