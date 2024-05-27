#!/usr/bin/python3
"""Set up Blueprints"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__)
from.index import *
