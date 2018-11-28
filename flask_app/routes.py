"""
If adding a new route, make sure it belongs here and wouldn't make more sense
    in a controller. If you're making a call to Plaid or FB, a new route
    probably belongs in one of the controllers
    (not applicable if just renaming routes) - MA
"""

import plaid
from flask import render_template, request
from flask_app import APP
from flask_app import plaid_ctrl, db, errors, error_handlers

try:
    from keys import PLAID_API_KEYS
except IOError:
    print("Keys File not Found. Online Access")


@APP.route('/')
@APP.route('/dashboard')
def dashboard():
    """
    description
    """
    event_data = db.get_firebase_collection("events")
    donation_data = db.get_firebase_collection("donations")

    return render_template('dashboard.html', page="Dash",
                           event_data=event_data,
                           donation_data=donation_data,
                           plaid_public_key=PLAID_API_KEYS["plaid_public_key"])


@APP.route('/login')
def login():
    """
    description

    Going to move the notes below into separate authorization controller - MA
    """
    """
    Act management actions like changing pwd should be in separate route - MA

    if request.form.get('password') == DATA_CHANGE_KEY:
        id = request.form.get('id')[4:]

        if request.form.get('action') == 'delete':
            DB.child(table).child(id).remove()

        elif request.form.get('action') == 'submit':
            get_data, get_keys = data_from(table)
            data = {}
            for key in request.form.keys():
                if key in ('id', 'action', 'password'):
                    continue
                data[key] = request.form.get(key)

            DB.child(table).child(id).set(data)

        else:
            error = True
            error_data = "Password is incorrect"
    """
    return render_template('login.html')


@APP.route("/get_access_token", methods=['POST'])
def get_access_token():
    """
    public_token = None
    access_token = plaid_ctrl.get_access_token(public_token)
    return access_token
    """

    # print("get_access_token route")

    plaid_access_token = plaid_ctrl.get_access_token(request.form['public_token'])
    # return render_template('dashboard.html', page="Dash",
    #                        event_data=event_data,
    #                        donation_data=donation_data)
    return "Something"


@APP.route('/forms', methods=['GET'])
def get_forms():
    """
    description
    """
    white_listed_forms = db.get_firebase_collection("forms")
    return render_template('forms.html', forms=white_listed_forms)


@APP.route('/data', methods=['POST', 'GET'])
def get_table_data():
    """
    Description
    """

    documents_data = {}
    collection = db.sanitize_user_input(request.args.get('table'))

    if collection is None:
        collection = "donations"

    documents_data = db.get_firebase_collection(collection)
    return render_template('table_data.html',
                           data=documents_data,
                           page=collection)


@APP.route('/update', methods=['POST', 'GET'])
def update():
    """
    description

    Same as above method, needs more description. Whats being updated? - MA
    """
    collection = db.sanitize_user_input(request.args.get('table'))
    return db.get_firebase_collection(collection)


@APP.route('/on_app_load')
def on_app_load():
    """
    description

    See above ^  - MA
    """
    pass
