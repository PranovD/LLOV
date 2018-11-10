""" PLEASE DON'T CHANGE LINES 1-16 - MA """

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
        conceptualized (See notes on method below) - MA

    I think we should instead create standard getters & setters for donations,
        events, and dogs, but the modular aspect of how this method works in
        terms of the /data route would be an excellent set up for requesting
        data from volunteers/fosters/& donors. Currently, there is a general
        "Profile" collection in Firebase where basic info such as
        name, email, etc is stored for all people. There are
        separate collections for volunteers, fosters, & donors that store the
        attributes that are specific to each group. Because of the way it's
        setup in there currently, I think this would work very well for
        requesting people related collections. - MA
    """
    return {'test1': sanitize_user_input(request1),
            'test2': sanitize_user_input(request2),
            'test3': 'test3'
            }


def get_dashboard_data():
    """
    Calls the relevant methods to populate a data object for the dashboard.
        This object is returned and later on is divided into more specific
        variables in templates using Jinja.

    Method created when I was trying to separate application layers,
        particularly to help replace data_from() method - MA
    """
    data = {}
    data['events'] = get_events()
    data['donations'] = get_donations()

    return data


def get_donations():
    """
    Retrieves "donations" collection in Firebase and returns as a JSON object

    Not sure if this returns a JSON object or pyre-object (whatever)? - MA
    """
    return DB.child("donations").get()


def add_foster_dog(data):
    """
    Adds a new foster dog to the "dogs" collection in Firebase based on the
        passed in data
    """

    clean_foster_data = sanitize_data(data)
    DB.child("fosterdogs").push(clean_foster_data)


def add_donation(data):
    """
    Adds a donation to the "donations" collection in Firebase based on the
        passed in data after the transaction is successful

    ALL donations should be added to the corresponding account
        BEFORE being added to firebase. So this method shoud ONLY be called
        after the add donation method from plaid_ctrl.py is called! Ex:
        New donation is being made. We pass the amount through the plaid_ctrl
        add_donation() method and the Plaid API takes care of the actual
        transaction, all we have to do is make the POST request (by calling
        the add_donation() method in plaid_ctrl). AFTER the transaction is
        successful, we can figure out how to write this method so that it
        asynchronously updates firebase. - MA
    """

    # See above notes - MA
    # DB.child("donations").push(data)

    return None


def get_events():
    """
    Retrieves "events" collection in Firebase and returns as a JSON object

    not sure if this returns a JSON object or pyre-object (whatever)? - MA
    """

    return DB.child("events").get()


def add_foster(data):
    """
    Adds a foster volunteer with passed in data to "volunteers"
        collection in Firebase
    """
    clean_data = sanitize_data(data)
    DB.child("fosters").push(clean_data)


def add_volunteer(data):
    """
    Adds a volunteer with passed in data to "volunteers" collection in Firebase
    """
    clean_data = sanitize_data(data)
    DB.child("volunteers").push(clean_data)


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
