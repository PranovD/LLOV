""" PLEASE DON'T CHANGE LINES 1-16 - MA """

import pyrebase
from flask_app import errors, mc_ctrl

try:
    from keys import FIREBASE_KEYS
except IOError:
    print("Keys File not Found. Online Access")

FIREBASE = pyrebase.initialize_app(FIREBASE_KEYS)
FIREBASE_AUTH = FIREBASE.auth()
FIREBASE_USER = FIREBASE_AUTH.sign_in_with_email_and_password(
                                                             "tester@llov.com",
                                                             "tester")
DB = FIREBASE.database()
white_listed_collections = ["Dogs", "Person", "donations", "events", "forms"]


def get_firebase_collection(collection):
    """
    Makes a get call to FireBase based on what collection the user wants to see
    Checks requested collection against a whitelist of available collections
    """

    if collection not in white_listed_collections:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    return DB.child(collection).get().val()


def add_firebase_document(collection, data):
    """
    Description
    """

    clean_data = sanitize_data(data)
    clean_collection = sanitize_user_input(collection)

    if clean_collection not in white_listed_collections:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    try:
        DB.child(clean_collection).push(clean_data)

    except:
        raise errors.InvalidUsage("We could not add your information \
                                  at this time.", status_code=410)


def sanitize_user_input(user_input):
    """
    Sanitizes passed in string as a security measure.

    Need to add actual sanitization code here, will work on this later - MA
    """
    return user_input


def sanitize_data(data):
    """
    Santitizes JSON objects, method chained with sanitize_user_input which
        takes in & returns strings.

    Actual security precautions need to be added here
        for authentic input sanitization. Will do later lol - MA
    """

    for key, value in data:
        if value is None:
            raise errors.InvalidUsage('All fields must be filled',
                                      status_code=410)
        else:
            key = sanitize_user_input(key)
            value = sanitize_user_input(value)
    return data
