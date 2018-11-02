""" This module does blah blah blah """

import pyrebase

try:
    import keys
    if keys.VERSION != "2.0":
        print("Download newest version of keys.py from the Google Drive")
except:
    print("Keys File not Found. Online Access")


FIREBASE = pyrebase.initialize_app(keys.FIREBASE_KEYS)
FIREBASE_AUTH = FIREBASE.auth()
FIREBASE_USER = FIREBASE_AUTH.sign_in_with_email_and_password(
                                                             "tester@llov.com",
                                                             "tester")
DB = FIREBASE.database()


def data_from(collection):
    """
    description
    """

    donation_data = [{'key': item.key(), 'val': item.val()} for item in
                     DB.child(collection).get().each()]
    donation_keys = [key.lower() for key in donation_data[0]['val'].keys()]
    return donation_data, donation_keys


def add_foster_dog(data):
    """
    description
    """
    DB.child("fosterdogs").push(data)


def sanitize_user_input(user_input):
    """
    description
    """
    return user_input
