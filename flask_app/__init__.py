""" This module does blah blah blah """

# import pyrebase
from flask import Flask


APP = Flask(__name__)

# config = {
#     "apiKey": "AIzaSyDcDBFlo7393yFlguGHl3pFLAZannyGmGA",
#     "authDomain": "llov-5592a.firebaseapp.com",
#     "databaseURL": "https://llov-5592a.firebaseio.com",
#     "storageBucket": "llov-5592a.appspot.com"
# }

# try:
#     from app import keys
# except IOError:
#     print("Keys File not Found. Online Access")
#
# FIREBASE = keys.FIREBASE_KEYS
# firebase = pyrebase.initialize_app(config)
# AUTH = FIREBASE.auth()
# FB_USER = AUTH.sign_in_with_email_and_password("tester@llov.com", "tester")
#
# DB = FIREBASE.database()
# DB = None


if __name__ == '__main__':
    APP.run(host='localhost')

from flask_app import routes
