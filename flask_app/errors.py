""" This module does blah blah blah """

# from flask import jsonify

class InvalidUsage(Exception):
    """
    description
    """
    status_code = 410

    def __init__(self, message, status_code=None, payload=None):
        """
        description
        """
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        description
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
