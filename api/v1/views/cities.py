#!/usr/bin/python3
""" restful api for class city """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ retrieve list of all city objects of a state """
    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieves a single city object by it's id """
    city = storage.get(City, city_id)
    if not city or city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city object by it's id """
    city = storage.get(City, city_id)
    if not city or city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city object in a state """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if not data or data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    data['state_id'] = state.id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates a city object using it's id """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if not data or data is None:
        return jsonify({"error": "Not a JSON"}), 400
    city = storage.get(City, city_id)
    if not city or city is None:
        abort(404)

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
