#!/usr/bin/python3
"""
Create index.py to connect to API
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """
    API status
    """
    response = ('status': "OK")
    return jsonify(response)

