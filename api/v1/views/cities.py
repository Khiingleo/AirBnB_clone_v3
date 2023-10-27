#!/usr/bin/python3
"""
    THis Module all default RESTFul API actions for Cities
    Author: Peter Ekwere
"""
import json
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort

@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """ This function returns all cities associated with a state """
    print(f"state id is {state_id}")
    a_list = []
    a_state = storage.get(State, state_id)
    if a_state == None:
        print(f"a state is {a_state}")
        abort(404)
    for city in a_state.cities:
        a_list.append(city.to_dict())
    return a_list
