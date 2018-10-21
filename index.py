from flask import Flask, request, render_template, json, jsonify
import os
import pymongo
import pyrebase
import datetime
import json
import pandas as pd

try:
    from keys import keys
except:
    print("Keys File not Found. Online Access")

API_KEY = os.environ.get('API_KEY') or keys['api_key']
AUTH_DOMAIN = os.environ.get('AUTH_DOMAIN') or keys['auth_domain']
DB_URL = os.environ.get('DB_URL') or keys['db_url']
PROJECT_ID = os.environ.get('PROJECT_ID') or keys['project_id']
STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET') or keys['storage_bucket']
MESSAGING_SENDER_ID = os.environ.get('MESSAGING_SENDER_ID') or keys['messaging_sender_id']
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT') or keys['service_account']


config = {
  "apiKey": API_KEY,
  "authDomain": AUTH_DOMAIN,
  "databaseURL": DB_URL,
  "projectId": PROJECT_ID,
  "storageBucket": STORAGE_BUCKET,
  "messagingSenderId": MESSAGING_SENDER_ID,
  "serviceAccount": SERVICE_ACCOUNT
}

app = Flask(__name__)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("tester@llov.com", "tester")
db = firebase.database()


@app.route('/')
def index():
    table = "donations"
    donnation_data, donnation_keys = dataFrom(table)
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
        donation_types_graph[donation['val']['source']] += float(donation['val']['amount'])
    donation_dates, donation_amounts = zip(*sorted(zip(donation_dates, donation_amounts)))
    table = "events"
    event_data, event_keys = dataFrom(table)
    return render_template('main.html', donation_pie_labels = donation_types_graph.keys(), donation_pie_values = donation_types_graph.values(), donation_dates=donation_dates, donation_amounts=donation_amounts, donation_graph_data=donnation_data, donation_amount=donation_amount, event_data=event_data, event_keys=event_keys,  page="Main")

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dog', methods = ['POST', 'GET'])
def postToDog():
    error = False
    errorData = ""
    if request.method == 'POST':
        name = request.form.get('dogName') # TEXT BOX
        gender = request.form.get('gender') # RADIO BUTTON
        age = request.form.get('age')
        weight = request.form.get('weight')
        breed = request.form.get('breed')
        comments = request.form.get('comments')
        diseases = request.form.get('diseases')
        dogAggressive = request.form.get('dog-aggressive')

        if name == None or len(name) == 0 or age == None or len(age) == 0 \
        or weight == None or len(weight) == 0 or breed == None or len(breed) == 0:
            error = True
            errorData = "All fields must be filled out."

        if not error:
            data = {
                'age': int(age),
                'breed': breed,
                'gender': gender,
                'name': name,
                'weight': int(weight),
                'comments': comments.split(","),
                'diseases': diseases,
                'dog_aggressive': dogAggressive,
                'date_added': str(datetime.datetime.now())
            }
            db.child("fosterdogs").push(data)

    return render_template('dog.html', page="Foster Dog", error=error, errorData=errorData)


@app.route('/volunteer', methods = ['POST', 'GET'])
def volunteers():
    error = False
    errorData = ""
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
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
        shortterm= request.form.get('short-term-foster')
        emergency= request.form.get('emergency-foster')
        coord= request.form.get('coordinating')
        flyers= request.form.get('putting-up-flyers')
        dogwalking= request.form.get('dog-walking')
        fundraising= request.form.get('fundraisers')
        adoptions= request.form.get('helping-at-adoptions')
        transporting= request.form.get('transporting')
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

        db.child("volunteers").push(data)

    return render_template('volunteer.html', page="Volunteers", error=error, errorData=errorData)


@app.route('/foster', methods = ['POST', 'GET'])
def postToFosters():
    error = False
    errorData = ""
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        phone = request.form.get('number')
        canAdoptMore = request.form.get('source')
        comments = request.form.get('comments')

        if first_name == None or len(first_name) == 0 or last_name == None or len(last_name) == 0:
            error = True
            errorData = "All fields must be filled out."

        if not error:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'street': street,
                'city': city,
                'state': state,
                'zipcode': zipcode,
                'canAdoptMore': canAdoptMore,
                'comments': comments,
                'timestamp': str(datetime.datetime.now())
            }
            db.child("fosters").push(data)

    return render_template('foster.html', page="Fosters", error=error, errorData=errorData)

@app.route('/donation', methods = ['POST', 'GET'])
def postToDonation():
    error = False
    errorData = ""
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        amount = request.form.get('amount')
        source = request.form.get('source')
        comments = request.form.get('comments')

        if first_name == None or last_name == None or source == None \
        or len(first_name) == 0 or len(source) == 0 or len(last_name) == 0:
            error = True
            errorData = "All fields must be filled out."

        if not error:
            try:
                amount = float(amount)

            except:
                error = True
                errorData = "Amount field has to be a valid $ amount."

        if not error:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'amount': amount,
                'comments': comments,
                'source': source,
                'timestamp': str(datetime.datetime.now())
            }
            db.child("donations").push(data)

    return render_template('donation.html', page="Donations", error=error, errorData=errorData)

@app.route('/data', methods = ['POST', 'GET'])
def returnData():
    table = request.args.get('table')
    if table is None:
        table = "donations"

    error = False
    errorData = ""

    if request.method == 'POST':
        if request.form.get('password') == DATA_CHANGE_KEY:
            id = request.form.get('id')[4:]

            if request.form.get('action') == 'delete':
                db.child(table).child(id).remove()

            elif request.form.get('action') == 'submit':
                data = {}
                for key in request.form.keys():
                    if key == 'id' or key == 'action' or key == 'password':
                        continue
                    data[key] = request.form.get(key)

                db.child(table).child(id).set(data)
        else:
            error = True
            errorData = "Password is incorrect"

    getData, keys = dataFrom(table)
    return render_template('data.html', data=getData, keys=keys, page=table, error=error, errorData=errorData)

def dataFrom(collection):
    data = [{'key': item.key(), 'val': item.val()} for item in db.child(collection).get().each()]
    keys = [key.lower() for key in data[0]['val'].keys()]
    return data, keys


@app.route('/update', methods = ['POST', 'GET'])
def update():
    print(request.args)
    return returnData()

@app.route('/onAppLoad')
def onAppLoad():
    pass


if __name__ == '__main__':
    app.run(host='localhost')
