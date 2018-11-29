""" This module does blah blah blah """

import plaid
import os
import csv
from flask import json
from flask_app import errors, db


try:
    from keys import PLAID_API_KEYS
except IOError:
    print("Keys File not Found. Online Access")

client = plaid.Client(PLAID_API_KEYS['plaid_client_id'],
                            PLAID_API_KEYS["plaid_secret"],
                            PLAID_API_KEYS["plaid_public_key"],
                            PLAID_API_KEYS["plaid_env"])






def get_access_token(public_token):
    """
    Handles public_token from Link SignIn to get an Access Token
    Access Token is how we get any data about a specific Account from Plaid
    """

    exchange_response = client.Item.public_token.exchange(public_token)
    print(exchange_response)
    with open('flask_app/financial.csv', 'a+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([exchange_response['access_token'],
                         exchange_response['item_id'],
                         exchange_response['request_id']])
    return exchange_response
    


