""" This module does blah blah blah """

from flask import render_template
from flask_app import APP
from flask_app import errors

@APP.errorhandler(404)
def error_404(e):
    """
    description
    """
    return render_template('error_page.html', error=str(e)), 404


@APP.errorhandler(500)
def error_500():
    """
    description
    """
    return render_template('error_page.html', error=str(e)), 404


@APP.errorhandler(errors.InvalidUsage)
def handle_invalid_usage():
    """
    description
    """
    # response = jsonify(error.to_dict())
    # response.status_code = error.status_code
    return render_template('invalid_usage_error.html'), 410
