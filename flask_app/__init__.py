""" This module does blah blah blah """

import pyrebase
from flask import Flask
try:
    import keys
except IOError:
    print("Keys File not Found. Online Access")

FIREBASE = pyrebase.initialize_app(keys.FIREBASE_KEYS)
FIREBASE_AUTH = FIREBASE.auth()
FIREBASE_USER = FIREBASE_AUTH.sign_in_with_email_and_password(
                                                             "tester@llov.com",
                                                             "tester")
DB = FIREBASE.database()
APP = Flask(__name__)

from flask_app import routes, db
