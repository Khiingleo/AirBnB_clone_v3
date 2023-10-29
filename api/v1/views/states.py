#!/usr/bin/python3
""" restful api for states class """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """ returns the state objects as json """
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ returns the state objects as json """
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ returns a state obj by it's id """
    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    result = state.to_dict()
    return jsonify(result)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state object by id """
    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@states.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new state object """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if not data or data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update a state object by id """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    data = request.get_json()
    if not data or data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ("id", "created_at", "updated_at"):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
