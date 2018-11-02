""" This module does blah blah blah """

import os
import datetime
import plaid
import pyrebase
from flask import Flask, request, render_template, json, jsonify
# import json
# import flask_login
# import pandas as pd
# import pymongo

try:
    import keys
except:
    print("Keys File not Found. Online Access")

# PLAID API KEYS
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID') \
    or keys.PLAID_API_KEYS['plaid_client_id']
PLAID_SECRET = os.getenv('PLAID_SECRET') or keys.PLAID_API_KEYS['plaid_secret']
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY') \
    or keys.PLAID_API_KEYS['plaid_public_key']
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox') \
    or keys.PLAID_API_KEYS['plaid_env']
PLAID_VERS = os.getenv('PLAID_VERS') or keys.PLAID_API_KEYS['plaid_vers']
ACCESS_TOKEN = None
CLIENT = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV,
                      api_version=PLAID_VERS)

# response = client.Item.public_token.exchange(public_token)
# access_token = response['access_token']

# FIREBASE KEYS
API_KEY = os.environ.get('API_KEY') or keys.FIREBASE_KEYS['api_key']
AUTH_DOMAIN = os.environ.get('AUTH_DOMAIN') \
    or keys.FIREBASE_KEYS['auth_domain']
DB_URL = os.environ.get('DB_URL') or keys.FIREBASE_KEYS['db_url']
PROJECT_ID = os.environ.get('PROJECT_ID') or keys.FIREBASE_KEYS['project_id']
STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET') \
    or keys.FIREBASE_KEYS['storage_bucket']
MESSAGING_SENDER_ID = os.environ.get('MESSAGING_SENDER_ID') \
    or keys.FIREBASE_KEYS['messaging_sender_id']
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT') \
    or keys.FIREBASE_KEYS['service_account']
DATA_CHANGE_KEY = os.environ.get('DATA_CHANGE_KEY') \
    or keys.FIREBASE_KEYS['data_change_key']


FIREBASE_CONFIG = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,
    "databaseURL": DB_URL,
    "projectId": PROJECT_ID,
    "storageBucket": STORAGE_BUCKET,
    "messagingSenderId": MESSAGING_SENDER_ID,
    "serviceAccount": SERVICE_ACCOUNT
}

app = Flask(__name__)
FIREBASE = pyrebase.initialize_app(FIREBASE_CONFIG)
AUTH = FIREBASE.auth()
USER = AUTH.sign_in_with_email_and_password("tester@llov.com", "tester")
DB = FIREBASE.database()


@app.route('/')
def index():
    """
    description
    """

    table = "donations"
    donnation_data, donation_keys = data_from(table)
    donation_amount = 0
    donation_dates = []
    donation_amounts = []
    donation_types_graph = {'Cash': 0, 'Check': 0, 'Venmo': 0, 'Cashapp': 0}
    for donation in donnation_data:
        donation_amount += float(donation['val']['amount'])
        date = donation['val']['timestamp'].split()
        date = date[0].split('-')
        date = date[1] + '-' + date[2] + '-' + date[0]
        donation_dates.insert(0, date)
        donation_amounts.insert(0, float(donation['val']['amount']))
        donation_types_graph[donation['val']['source']] \
            += float(donation['val']['amount'])
    donation_dates, donation_amounts = zip(*sorted(zip(donation_dates,
                                                       donation_amounts)))
    table = "events"
    event_data, event_keys = data_from(table)
    return render_template('main.html',
                           donation_pie_labels=donation_types_graph.keys(),
                           donation_pie_values=donation_types_graph.values(),
                           donation_dates=donation_dates,
                           donation_amounts=donation_amounts,
                           donation_graph_data=donnation_data,
                           donation_amount=donation_amount,
                           event_data=event_data,
                           event_keys=event_keys,
                           page="Main")


@app.route('/login')
def login():
    """
    description
    """

    return render_template('login.html')


@app.route('/dog', methods=['POST', 'GET'])
def post_to_dog():
    """
    description
    """

    error = False
    error_data = ""

    if request.method == 'POST':
        name = request.form.get('dogName')
        gender = request.form.get('gender')
        age = request.form.get('age')
        weight = request.form.get('weight')
        breed = request.form.get('breed')
        comments = request.form.get('comments')
        diseases = request.form.get('diseases')
        dog_aggressive = request.form.get('dog-aggressive')

        if name is None or not name or age is None or not age \
            or weight is None or not weight or breed is None \
                or not breed:
            error = True
            error_data = "All fields must be filled out."

        if not error:
            data = {
                'age': int(age),
                'breed': breed,
                'gender': gender,
                'name': name,
                'weight': int(weight),
                'comments': comments.split(","),
                'diseases': diseases,
                'dog_aggressive': dog_aggressive,
                'date_added': str(datetime.datetime.now())
            }
            DB.child("fosterdogs").push(data)

    return render_template('dog.html', page="Foster Dog",
                           error=error, error_data=error_data)


@app.route('/volunteer', methods=['POST', 'GET'])
def volunteers():
    """
    description
    """

    error = False
    error_data = ""

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        # email = request.form.get('email')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        number = request.form.get('number')

        # commitment
        volunteering = request.form.get('volunteering')
        fostering = request.form.get('fostering')
        adopting = request.form.get('adopting')

        # volunteering
        longterm = request.form.get('long-term-foster')
        shortterm = request.form.get('short-term-foster')
        emergency = request.form.get('emergency-foster')
        coord = request.form.get('coordinating')
        flyers = request.form.get('putting-up-flyers')
        dogwalking = request.form.get('dog-walking')
        fundraising = request.form.get('fundraisers')
        adoptions = request.form.get('helping-at-adoptions')
        transporting = request.form.get('transporting')
        vet = request.form.get('vet-appointments')
        volunteering_other = request.form.get('volunteering-other')

        # foster_requirements
        female = request.form.get('female')
        male = request.form.get('male')
        small = request.form.get('small')
        large = request.form.get('large')
        breeds = request.form.get('breeds')
        fostering_other = request.form.get('fostering-other')

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'street': street,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'phone_number': number,
            'volunteering': {
                'can_volunteer': volunteering,
                'longterm': longterm,
                'shortterm': shortterm,
                'emergency': emergency,
                'coord': coord,
                'flyers': flyers,
                'dogwalking': dogwalking,
                'fundraising': fundraising,
                'adoptions': adoptions,
                'transporting': transporting,
                'vet': vet,
                'other': volunteering_other,
            },
            'adoption_fostering': {
                'can_adopt': adopting,
                'can_foster': fostering,
                'dogTypes': {
                    'female': female,
                    'male': male,
                    'small': small,
                    'large': large,
                    'breeds': breeds,
                    'other': fostering_other
                }
            }
        }

        DB.child("volunteers").push(data)

    return render_template('volunteer.html', page="Volunteers",
                           error=error, error_data=error_data)


@app.route('/foster', methods=['POST', 'GET'])
def post_to_fosters():
    """
    description
    """

    error = False
    error_data = ""

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        # phone = request.form.get('number')
        can_adopt_more = request.form.get('source')
        comments = request.form.get('comments')

        if first_name is None or not first_name or last_name is None \
                or not last_name:
            error = True
            error_data = "All fields must be filled out."

        if not error:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'street': street,
                'city': city,
                'state': state,
                'zipcode': zipcode,
                'can_adopt_more': can_adopt_more,
                'comments': comments,
                'timestamp': str(datetime.datetime.now())
            }
            DB.child("fosters").push(data)

    return render_template('foster.html', page="Fosters", error=error,
                           error_data=error_data)


@app.route('/donation', methods=['POST', 'GET'])
def postToDonation():
    """
    description
    """

    error = False
    error_data = ""

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        amount = request.form.get('amount')
        source = request.form.get('source')
        comments = request.form.get('comments')

        if first_name is None or last_name is None or source is None \
                or not first_name or not source \
                or not last_name:
            error = True
            error_data = "All fields must be filled out."

        if not error:
            try:
                amount = float(amount)

                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'amount': amount,
                    'comments': comments,
                    'source': source,
                    'timestamp': str(datetime.datetime.now())
                }

                DB.child("donations").push(data)

            except:
                error = True
                error_data = "Amount field has to be a valid $ amount."

    return render_template('donation.html', page="Donations",
                           error=error, error_data=error_data)


@app.route('/data', methods=['POST', 'GET'])
def return_data():
    """
    description
    """

    get_data = None
    balance = None
    error = False
    error_data = ""
    get_keys = None
    table = request.args.get('table')

    if table is None:
        table = "donations"

    if table == "donations":
        try:
            balance_response = CLIENT.Accounts.balance.get(ACCESS_TOKEN)
            balance = json.dumps(balance_response, indent=2,
                                 sort_keys=True)

        except plaid.errors.PlaidError as err:
            error = True
            error_data = jsonify({'error': {'display_message':
                                            err.display_message,
                                            'error_code': err.code,
                                            'error_type': err.type}})

    """
    Account management actions like changing pwd should be in separate route

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

    get_data, get_keys = data_from(table)
    return render_template('data.html', data=get_data, get_keys=get_keys,
                           page=table, error=error, error_data=error_data,
                           balance=balance)


def data_from(collection):
    """
    description
    """

    data = [{'key': item.key(), 'val': item.val()}
            for item in DB.child(collection).get().each()]
    keys = [key.lower() for key in data[0]['val'].keys()]
    return data, keys


@app.route('/update', methods=['POST', 'GET'])
def update():
    """
    description
    """

    print(request.args)
    return return_data()


@app.route('/on_app_load')
def on_app_load():
    """
    description
    """

    pass


if __name__ == '__main__':
    app.run(host='localhost')
