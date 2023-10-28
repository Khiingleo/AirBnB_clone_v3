#!/usr/bin/python3
""" restful api for the Users class """

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def users():
    """ returns user in JSON format """
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<string:user_id>",
                 methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """ returns user and the user id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """ deletes a user based on it's id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def user_create():
    """ creates a new user """
    data = request.get_json()
    if not data or data is None:
        abort(400, 'Not a JSON')
    if not data.get('email'):
        abort(400, 'Missing email')
    if not data.get('password'):
        abort(400, 'Missing password')
    new_user = User(**data)
    storage.new(new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates an existing state object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    user_data = request.get_json()
    if not user_data or user_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    user_obj.api_update(user_data)
    storage.new(user_obj)
    storage.save()
    return jsonify(user_obj.to_dict()), 200
