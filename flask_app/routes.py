""" Description """

from flask import render_template, request
from flask_app import APP
from flask_app import plaid_ctrl, db

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

    request.form.get('inputPassword')

            error = True
            error_data = "Password is incorrect"
    """
    return render_template('login.html')


@APP.route('/forms', methods=['GET'])
def get_forms():
    """
    description
    """
    white_listed_forms = db.get_firebase_collection("forms")
    return render_template('forms.html',
                           forms=white_listed_forms)


@APP.route('/forms', methods=['POST'])
def edit_form_link():
    """
    description
    """
    form_id = db.sanitize_user_input(request.form.get('form_id'))
    form_name = db.sanitize_user_input(request.form.get('form_name'))
    new_form_link = db.sanitize_user_input(request.form.get('new_form_link'))

    updated_form_data = {'form_name': form_name, 'form_link': new_form_link}
    db.update_firebase_document("forms", form_id, updated_form_data)

    return get_forms()


@APP.route("/get_access_token", methods=['POST'])
def get_access_token():
    """
    public_token = None
    access_token = plaid_ctrl.get_access_token(public_token)
    return access_token
    """

    plaid_access_token = plaid_ctrl.get_access_token(
        request.form['public_token'])
    # return render_template('dashboard.html', page="Dash",
    #                        event_data=event_data,
    #                        donation_data=donation_data)
    return "Something"


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
