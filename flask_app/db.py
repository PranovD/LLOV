""" PLEASE DON'T CHANGE LINES 1-17 """

import pyrebase
from flask_app import errors

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


def data_from(request1, request2):
    """
    Temporary method that will be removed once data calls are better
        conceptualized (See notes on method below)
    """
    return {'test1': sanitize_user_input(request1),
            'test2': sanitize_user_input(request2),
            'test3': 'test3'
            }


def get_dashboard_data():
    data = {}
    data['events'] = get_events()
    data['donations'] = get_donations()

    return data


def get_donations():
    """
    description
    """
    return DB.child("donations").get()


def add_foster_dog(data):
    """
    description
    """

    clean_foster_data = sanitize_data(data)
    DB.child("fosterdogs").push(clean_foster_data)


def add_donation(data):
    """
    ALL donations should be added to the corresponding account
        BEFORE being added to firebase. So this method shoud ONLY be called
        after the add donation method from plaid_ctrl.py is called! Ex:
        New donation is being made. We pass the amount through the plaid_ctrl
        add_donation() method and the Plaid API takes care of the actual
        transaction, all we have to do is make the POST request (by calling
        the add_donation() method in plaid_ctrl). AFTER the transaction is
        successful, we can figure out how to write this method so that it
        asynchronously updates firebase.
    """

    # See above notes
    # DB.child("donations").push(data)

    return None


def get_events():
    """
    description
    """

    return DB.child("events").get()


def add_foster(data):
    """
    description
    """
    clean_data = sanitize_data(data)
    DB.child("fosters").push(clean_data)


def add_volunteer(data):
    """
    description
    """
    clean_data = sanitize_data(data)
    DB.child("volunteers").push(clean_data)


def sanitize_user_input(user_input):
    """
    description
    """
    return user_input


def sanitize_data(data):
    """
    description
    """

    for key, value in data:
        if value is None:
            raise errors.InvalidUsage('All fields must be filled', status_code=410)
        else:
            key = sanitize_user_input(key)
            value = sanitize_user_input(value)

    return data
