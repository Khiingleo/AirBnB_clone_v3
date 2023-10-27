#!/usr/bin/python3
""" flask application with status route and stats route """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ returns a JSON of OK status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    class_stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
    }
    return jsonify(class_stats)
