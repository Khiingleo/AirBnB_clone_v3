#!/usr/bin/python3

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response
from os import getenv
import json


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """closes session"""
    storage.close()


@app.errorhandler(404)
def not_found_404(error):
    """handler for 404 errors"""
    response = make_response(json.dumps({'error': 'Not found'},
                             indent=2) + "\n")
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
