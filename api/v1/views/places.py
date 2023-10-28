#!/usr/bin/python3
""" restful api for place class """
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_cities(city_id):
    """
    retrieves the list of all place objects of a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ returns a place object using it's id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ deletes a place based on it's id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_create(city_id):
    """ creates a place using the city id """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif "name" not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": 'Missing user_id'}), 400
    else:
        place_data = request.get_json()
        city = storage.get(City, city_id)
        user = storage.get(User, place_data['user_id'])
        if city is None or user is None:
            abort(404)
        place_data['city_id'] = city.id
        place_data['user_id'] = user.id
        place_obj = Place(**place_data)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place object """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    place_data = request.get_json()
    ignore = ("id", "user_id", "created_at", "updated_at")
    for key, value in place_data.items():
        if key not in ignore:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
