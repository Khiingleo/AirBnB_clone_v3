#!/usr/bin/python3
"""
    restful api from the amenity class
    Author: Peter
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ retrieve a list of all amenity objects """
    amenities_list = [a.to_dict() for a in storage.all(Amenity).values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a single Amenity object by it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity or amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an Amenity object by it's ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity or amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ creates a new amenity object """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object by ID"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    amenity = storage.get(Amenity, amenity_id)
    if not amenity or amenity is None:
        abort(404)
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
