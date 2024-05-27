#!/usr/bin/python3
"""
New view for Review object that handles all default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.review import Review
from models.place import Place
from models import storage


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def getAllReviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    review_list = [review.to_dict() for review in storage.all(
        'Review').values() if review.place_id == place_id]
    return jsonify(review_list)


@app_views.route(
        '/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def getReview(review_id):
    """Retrieves a specific Review object by ID"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404, description="Review not found")
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def DEL_review(review_id):
    """Deletes a specific Review object by ID"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404, description="Review not found")

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def POST_review(place_id):
    """Creates a new Review object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    required_fields = ['user_id', 'text']

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404, description="User not found")

    place = storage.get("Place", place_id)
    if place is None:
        abort(404, description="Place not found")

    new_review = Review(**data)
    new_review.place_id = place_id
    storage.new(new_review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def PUT_review(review_id):
    """Updates a specific Review object by ID"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404, description="Review not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "place_id", "user_id", "created_at", "updated_at"]
    data = request.get_json()

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
