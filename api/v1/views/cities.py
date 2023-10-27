#!/usr/bin/python3
"""
    THis Module all default RESTFul API actions for Cities
    Author: Peter Ekwere
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """ This function returns all cities associated with a state """
    a_list = []
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)
    for city in a_state.cities:
        a_list.append(city.to_dict())
    return jsonify(a_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """ This function returns a city based on the id """
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    return jsonify(a_city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletes a state based on it's id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ creates a new city """
    A_state = storage.get(State, state_id)
    data = request.get_json()
    if A_state is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    data["state_id"] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ updates an existing city """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    obj_data = request.get_json()
    city_obj.name = obj_data['name']
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
