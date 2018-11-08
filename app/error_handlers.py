""" This module does blah blah blah """

from flask import render_template
from app import app
from . import errors


@app.errorhandler(404)
def not_found_error():
    """
    description
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error():
    """
    description
    """
    return render_template('500.html'), 500


@app.errorhandler(errors.InvalidUsage)
def handle_invalid_usage():
    """
    description
    """
    # response = jsonify(error.to_dict())
    # response.status_code = error.status_code
    return render_template('invalid_usage_error.html'), 410
