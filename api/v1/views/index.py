#!/usr/bin/python3
""" flask app with routes status and stats """
from api.v1.views import app_views
from flask import jsonify, request
import json
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.place import Place


@app_views.route("/status")
def status():
    """ returns a JSON OK status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=['GET'])
def stats():
    """ returns the count of all classes in the storage """
    if request.method == 'GET':
        classes = {"amenities": Amenity, "cities": City, "places": Place,
                   "reviews": Review, "states": State, "users": User}
        class_stats = {}
        for key, value in classes.items():
            class_stats[key] = storage.count(value)
        return json.dumps(class_stats, indent=2) + "\n"
