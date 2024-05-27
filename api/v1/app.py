#!/usr/bin/python3
"""
Initialize Flask Application
"""
import os
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """closes current session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handles 404 errors by returning a JSON formatted response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
