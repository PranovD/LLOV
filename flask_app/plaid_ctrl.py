""" This module does blah blah blah """

import plaid
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

# PLAID_ACCESS_TOKEN = PLAID_API_KEYS["plaid_access_token"]


access_token = None
public_token = None

def get_plaid_data():
    """
    description
    """
    try:
        balance_response = \
            None
#           PLAID_CLIENT.Accounts.balance.get(PLAID_ACCESS_TOKEN)
        balance = json.dumps(balance_response, indent=2, sort_keys=True)
        return balance

    except plaid.errors.PlaidError:
        raise errors.InvalidUsage('This view is gone', status_code=410)


def get_plaid_donations(request):
    """
    description
    """

def get_access_token(public_token):
    global access_token
    exchange_response = client.Item.public_token.exchange(public_token)
    print('access token: ' + exchange_response['access_token'])
    print('item ID: ' + exchange_response['item_id'])
    print(exchange_response)

    return exchange_response
