#!/usr/bin/python3
"""
    restful api for states class

"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ returns the state objects as json """
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ returns a state obj by it's id """
    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    result = state.to_dict()
    return jsonify(result)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state object by id """
    state = storage.get(State, state_id)
    if not state or state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new state object """
    data = request.get_json()
    if not data():
        abort(400, "Not a JSON")
    elif "name" not in data:
        abort(400, "Missing name")
    else:
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                  strict_slashes=False)
def update_state(state_id):
    """ update a state object by id """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in data.items():
        if key not in ("id", "created_at", "updated_at"):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
