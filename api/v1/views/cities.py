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
    if not a_state or a_state is None:
        abort(404)
    for city in a_state.cities:
        a_list.append(city.to_dict())
    return jsonify(a_list), 200


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """ This function returns a city based on the id """
    a_city = storage.get(City, city_id)
    if not a_city or a_city is None:
        abort(404)
    return jsonify(a_city.to_dict()), 200


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletes a state based on it's id"""
    city = storage.get(City, city_id)
    if not city or city is None:
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
    if not data or data is None:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing name')
    data["state_id"] = state_id
    new_city = City(**data)
    storage.new(City)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ updates an existing city """
    obj_data = request.get_json()
    if not obj_data or obj_data is None:
        abort(400, "Not a JSON")
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    city_obj.api_update(obj_data)
    return jsonify(city_obj.to_dict()), 200
