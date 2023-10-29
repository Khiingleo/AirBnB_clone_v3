#!/usr/bin/python3
"""
    THis Module handles all default RESTFul API actions for amenities
    Author: Peter Ekwere
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ This function returns all amenities """
    a_list = []
    all_amenities = storage.all(Amenity)
    for key, value in all_amenities.items():
        a_list.append(value.to_dict())
    return jsonify(a_list), 200


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """ This function returns an amenity based on the id """
    the_amenity = storage.get(Amenity, amenity_id)
    if not the_amenity or the_amenity is None:
        abort(404)
    return jsonify(the_amenity.to_dict()), 200


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes an amenity based on it's id"""
    the_amenity = storage.get(Amenity, amenity_id)
    if not the_amenity or the_amenity is None:
        abort(404)
    the_amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ creates a new amenity """
    data = request.get_json()
    if not data or data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ updates an existing amenity """
    amenity_data = request.get_json()
    if not amenity_data or amenity_data is None:
        abort(400, "Not a JSON")
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj.api_update(amenity_data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 200
