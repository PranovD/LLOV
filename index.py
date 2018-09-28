from flask import Flask, request, render_template, json
import os
import pymongo
import pyrebase
import datetime

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
    return render_template('main.html', page="Main")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dogs', methods = ['POST', 'GET'])
def dogs():
    if request.method == 'POST':
        name = request.form.get('dogName') # TEXT BOX
        gender = request.form['gender'] # RADIO BUTTON
        age = request.form.get('age')
        weight = request.form.get('weight')
        breed = request.form.get('breed')
        comments = request.form.get('comments')
        diseases = request.form.get('diseases')
        dogAggressive = request.form.get('dog-aggressive')
        humanAggressive = request.form.get('human-aggressive')

        data = {
            'Age': int(age),
            'Breed': breed,
            'Gender': gender,
            'Name': name,
            'Weight': int(weight),
            'characteristics':
                {'comments': comments.split(","),
                'diseases': diseases,
                'dog_aggressive': dogAggressive,
                'human_aggressive': humanAggressive},
            'date_added': str(datetime.datetime.now())
        }
        db.child("fosterdogs").push(data)

    dogData = db.child("fosterdogs").get()

    return render_template('fosterdogs.html', data=dogData, page="Foster Dogs")

@app.route('/volunteers', methods = ['POST', 'GET'])
def volunteers():
    if request.method == 'POST':
        print(request.form.get('firstName'))

    return render_template('volunteers.html', page="Volunteers")


@app.route('/fosters')
def fosters():
    pyreObj = db.child("fosters").get().val()
    data=[]
    for x, (key, value) in enumerate(pyreObj.items()):
        data.append(value)

    print(data)
    # print(fosterData.val())
    # print(type(fosterData))
    # print(type(fosterData.val()))
    return render_template('fosters.html', data=data, pyreObj=pyreObj, page="Foster Volunteers")


@app.route('/donations')
def donationsPage():
    return render_template('donations.html', page="Donations")


@app.route('/forms', methods=['GET'])
def formsPage():
    pass


@app.route('/data')
def dataPage():
    return json.jsonify(db.get().val())


@app.route('/onAppLoad')
def onAppLoad():
    pass


if __name__ == '__main__':
    app.run(host='localhost')
