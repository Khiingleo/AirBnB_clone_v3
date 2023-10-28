#!/usr/bin/python3
""" restful api for the State class """

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """ returns state in JSON format """
    states_list = []
    for state in storage.all('State').values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """ returns state and the state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """ deletes a state based on it's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def states_create():
    """ creates a new state """
    data = request.get_json()
    if data is None or not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates an existing state object"""
    obj_data = request.get_json()
    if not obj_data or obj_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    state_obj.api_update(obj_data)
    return jsonify(state_obj.to_dict()), 200
