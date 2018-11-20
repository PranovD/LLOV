"""
This module starts the application

Sensitive file, edit at your own risk lol  - MA
"""

from flask import Flask
from config import Config

APP = Flask(__name__)
APP.config.from_object(Config)

from flask_app import routes, db, forms_ctrl
