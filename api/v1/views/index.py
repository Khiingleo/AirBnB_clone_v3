#!/usr/bin/python3
""" djsdj """
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """ returns a JSON of OK status"""
    return jsonify({'status': 'Ok'})
