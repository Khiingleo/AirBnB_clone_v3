#!/usr/bin/python3
""" flask app with routes status and stats """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ returns a JSON OK status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """ returns the count of all classes in the storage """
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    class_stats = {}
    for key, value in classes.items():
        class_stats[key] = storage.count(value)
    return jsonify(class_stats)
