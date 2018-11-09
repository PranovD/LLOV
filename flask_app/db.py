""" This module does blah blah blah """

from app import app, DB
import pyrebase
# from . import errors
#
# try:
#     from . import keys
# except IOError:
#     print("Keys File not Found. Online Access")
#
#
# FIREBASE = pyrebase.initialize_app(keys.FIREBASE_KEYS)
# FIREBASE_AUTH = FIREBASE.auth()
# FIREBASE_USER = FIREBASE_AUTH.sign_in_with_email_and_password(
#                                                              "tester@llov.com",
#                                                              "tester")
# DB = FIREBASE.database()


def data_from(collection):
    """
    description
    """

    donation_data = [{'key': item.key(), 'val': item.val()} for item in
                     DB.child(collection).get().each()]
    donation_keys = [key.lower() for key in donation_data[0]['val'].keys()]
    return donation_data, donation_keys
#
#
# def add_foster_dog(data):
#     """
#     description
#     """
#     for key, value in data:
#         if value is None:
#             raise errors.InvalidUsage('This view is gone', status_code=410)
#         else:
#             key = sanitize_user_input(key)
#             value = sanitize_user_input(value)
#
#     DB.child("fosterdogs").push(data)
#
#
# def add_donation(data):
#     """
#     description
#     """
#
#     for key, value in data:
#         if value is None:
#             raise errors.InvalidUsage('This view is gone', status_code=410)
#         else:
#             key = sanitize_user_input(key)
#             value = sanitize_user_input(value)
#
#     DB.child("donations").push(data)
#
#
# def add_foster(data):
#     """
#     description
#     """
#     for key, value in data:
#         if value is None:
#             raise errors.InvalidUsage('This view is gone', status_code=410)
#         else:
#             key = sanitize_user_input(key)
#             value = sanitize_user_input(value)
#
#     DB.child("fosters").push(data)
#
#
# def add_volunteer(data):
#     """
#     description
#     """
#     for key, value in data:
#         if value is None:
#             raise errors.InvalidUsage('This view is gone', status_code=410)
#         else:
#             key = sanitize_user_input(key)
#             value = sanitize_user_input(value)
#
#     DB.child("volunteers").push(data)
#
#
# def sanitize_user_input(user_input):
#     """
#     description
#     """
#     return user_input
