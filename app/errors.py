from flask import render_template
from app import app, db



# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404

@app.errorhandler(invalid_usage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

