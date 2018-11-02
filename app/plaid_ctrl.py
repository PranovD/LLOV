""" This module does blah blah blah """

import plaid

try:
    import keys
    if keys.VERSION != "2.0":
        print("Download newest version of keys.py from the Google Drive")
except:
    print("Keys File not Found. Online Access")

PLAID_CLIENT = plaid.Client(keys.PLAID_API_KEYS['plaid_client_id'],
                            keys.PLAID_API_KEYS["plaid_secret"],
                            keys.PLAID_API_KEYS["plaid_public_key"],
                            keys.PLAID_API_KEYS["plaid_env"],
                            keys.PLAID_API_KEYS["plaid_vers"])
