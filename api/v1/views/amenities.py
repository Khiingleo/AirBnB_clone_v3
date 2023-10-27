#!/usr/bin/python3
"""
    THis Module handles all default RESTFul API actions for amenities
    Author: Peter Ekwere
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ This function returns all amenities """
    a_list = []
    all_amenities = storage.all(Amenity)
    for key, value in all_amenities.items():
        a_list.append(value.to_dict())
    return jsonify(a_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """ This function returns an amenity based on the id """
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    return jsonify(the_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes an amenity based on it's id"""
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    the_amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ creates a new amenity """
    data = request.get_json()
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ updates an existing amenity """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_data = request.get_json()
    amenity_obj.name = amenity_data['name']
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
