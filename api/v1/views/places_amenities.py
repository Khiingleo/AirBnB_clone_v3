#!/usr/bin/python3
"""Restful API for linking Place and Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
STORAGE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """Retrieve the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = [a.to_dict() for a in place.amenities]
    return jsonify(amenities_list), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)
    if (amenity not in place.amenities and
            amenity.id not in place.amenities):
        abort(404)
    if STORAGE == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenities.pop(amenity.id, None)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if (amenity not in place.amenities and
            amenity.id not in place.amenities):
        return jsonify(amenity.to_dict()), 200

    if STORAGE == 'db':
        place.amenities.append(amenity)
    else:
        place.amenities.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
