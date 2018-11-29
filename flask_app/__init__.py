"""
This module starts the application

Sensitive file, edit at your own risk lol  - MA
"""

from flask import Flask

APP = Flask(__name__)

from flask_app import routes, db
