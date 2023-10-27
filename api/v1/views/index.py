#!/usr/bin/python3
""" djsdj """
from api.v1.views import app_views
import json
from models import storage

@app_views.route("/status")
def status():
    """ returns a JSON of OK status"""
    return json.dumps({"status": "OK"}, indent=2) + "\n"

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
    response = json.dumps(class_stats, indent=2) + "\n"
    return response
