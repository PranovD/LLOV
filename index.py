from flask import Flask, request, render_template, jsonify
import os
import pymongo
import pyrebase

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
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/forms', methods=['GET'])
def formsPage():
    pass

@app.route('/data')
def dataPage():
    return jsonify(db.get().val())

@app.route('/donations')
def donationsPage():
    pass

@app.route('/onAppLoad')
def onAppLoad():
    pass

if __name__ == '__main__':
    app.run(host='localhost')




