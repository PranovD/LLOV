import plaid
import os
import csv
import pandas as pd
import datetime
import pyrebase
import pprint

try:
  from keys import PLAID_API_KEYS
  from keys import FIREBASE_KEYS
except IOError:
  print("Keys File not Found. Online Access")

client = plaid.Client(PLAID_API_KEYS['plaid_client_id'],
              PLAID_API_KEYS["plaid_secret"],
              PLAID_API_KEYS["plaid_public_key"],
              PLAID_API_KEYS["plaid_env"])

FIREBASE = pyrebase.initialize_app(FIREBASE_KEYS)
FIREBASE_AUTH = FIREBASE.auth()
FIREBASE_USER = FIREBASE_AUTH.sign_in_with_email_and_password(
                                                             "tester@llov.com",
                                                             "tester")
DB = FIREBASE.database()

df = pd.read_csv('flask_app/financial.csv')
print(df)
transactions_ids = {}

for index,row in df.iterrows():
    # response = client.Transactions.get(row['access_token'])
    # Pull transactions for the last day change in future
    start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-1))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    count = 0
    unique = 0
    try:
        transactions_response = client.Transactions.get(row['access_token'], start_date, end_date)
        for row in transactions_response['transactions']:
            
            if row['transaction_id'] not in transactions_ids and row['amount'] < 0:
                # print(row['transaction_id'])
                clean_transaction = {}
                clean_transaction['Amount'] = str(-row['amount'])
                clean_transaction['Comments'] = 'N/A'
                clean_transaction['Donor Name'] = row['name']
                clean_transaction['Date Given'] = datetime.datetime.strptime(row['date'], "%Y-%m-%d").strftime("%m/%d/%Y")
                clean_transaction['Source'] = 'Bank Transaction'
                # print(clean_transaction)
                DB.child('donations').push(clean_transaction)
                unique += 1
            transactions_ids[row['transaction_id']] = True
            count += 1
    except plaid.errors.PlaidError as e:
        print(e)
    except KeyError as e:
        print(str(e))
        pprint.pprint(transactions_response)
        break
    # print(transactions_response)


    
