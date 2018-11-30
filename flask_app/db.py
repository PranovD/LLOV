""" PLEASE DON'T CHANGE LINES 1-16 - MA """

import pyrebase
import sys
from flask_app import errors

try:
    from keys import FIREBASE_KEYS
except IOError:
    print("Keys File not Found. Online Access")

FIREBASE = pyrebase.initialize_app(FIREBASE_KEYS)
FIREBASE_AUTH = FIREBASE.auth()
FIREBASE_USER = FIREBASE_AUTH.sign_in_with_email_and_password(
                                                             "tester@llov.com",
                                                             "tester")
DB = FIREBASE.database()
white_listed_collections = ["Dogs", "Person", "donations", "events", "forms"]


def get_firebase_collection(collection):
    """
    Makes a get call to FireBase based on what collection the user wants to see
    Checks requested collection against a whitelist of available collections
    """

    if collection not in white_listed_collections:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    return DB.child(collection).get().val()


def add_firebase_document(collection, data):
    """
    Description
    """

    clean_data = sanitize_data(data)
    clean_collection = sanitize_user_input(collection)

    if clean_collection not in white_listed_collections:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    try:
        DB.child(clean_collection).push(clean_data)

    except:
        raise errors.InvalidUsage("We could not add your information \
                                  at this time.", status_code=410)


def update_firebase_document(collection, doc_id, data):
    """
    Description
    """
    # This doesn't work when passing in a form obj for some reason? See /forms post route
    # clean_data = sanitize_data(data)

    clean_collection = sanitize_user_input(collection)
    clean_doc_id = sanitize_user_input(doc_id)

    if clean_collection not in white_listed_collections:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    try:
        DB.child(clean_collection).child(clean_doc_id).update(data)

    except:
        raise errors.InvalidUsage("We could not add your information \
                                  at this time.", status_code=410)


def remove_firebase_document(collection, doc_id):
    """
    Description
    """

    clean_collection = sanitize_user_input(collection)
    clean_doc_id = sanitize_user_input(doc_id)

    try:
        DB.child(clean_collection).child(clean_doc_id).remove()

    except:
        raise errors.InvalidUsage("We could not remove your information \
                                  at this time.", status_code=410)


def sanitize_user_input(user_input):
    """
    Sanitizes passed in string as a security measure.

    Need to add actual sanitization code here, will work on this later - MA
    """
    return user_input


def sanitize_data(data):
    """
    Santitizes JSON objects, method chained with sanitize_user_input which
        takes in & returns strings.

    Actual security precautions need to be added here
        for authentic input sanitization. Will do later lol - MA
    """

    for key, value in data:
        if value is None:
            raise errors.InvalidUsage('All fields must be filled',
                                      status_code=410)
        else:
            key = sanitize_user_input(key)
            value = sanitize_user_input(value)
    return data


def get_donors_data():
    """
    donor_data = { donor_id: { total cont: num,
                               past trans: {},
                               donation cols pasted here
                              }
                  }
    """

    donor_data = {}
    donation_data = get_firebase_collection("donations")
    person_data = get_firebase_collection("Person")

    for donation_id, donation in donation_data.items():
        donor_id = donation['Donor ID']

        if donor_id not in donor_data:
            person = person_data.items()[donor_id]
            person['Total Contributions'] = donation['Amount']
            person['Past Transactions'] = {donation_id: donation}
            donor_data[donor_id] = person

        else:
            total_contr = int(donor_data[donor_id]['Total Contributions'])
            total_contr += int(donation['Amount'])
            donor_data[donor_id]['Total Contributions'] = total_contr.toString()
            donor_data[donor_id]['Past Transactions'][donation_id] = donation

    return donor_data


def get_formatted_donors_data():
    """
    Description
    """
    formatted_donors_data = []
    donors_data = get_donors_data()
    index = 0

    while donors_data:
        max_donor_id = max(donors_data,
                           key=lambda x: donors_data[x]['Total Contributions'])
        donor_name = donors_data[max_donor_id]['First Name'] + " " + donors_data[max_donor_id]['Last Name']
        donor_tot = donors_data[max_donor_id]['Total Contributions']
        donor_email = donors_data[max_donor_id]['Email']
        donor_phone = donors_data[max_donor_id]['Phone Number']
        formatted_donors_data[index] = [max_donor_id, donor_name, donor_tot,
                                        donor_email, donor_phone]

        donors_data.pop(max_donor_id, None)
        index += 1

    return formatted_donors_data

def donation_graph_data():
    table = "donations"
    donnation_data, donnation_keys = dataFrom(table)
    donation_amount = 0
    donation_dates = []
    donation_amounts = []
    donation_types_graph = {'Cash': 0, 'Check': 0, 'Venmo': 0, 'Cashapp': 0, 'Bank Transaction': 0}
    for donation in donnation_data:
        donation_amount += float(donation['val']['Amount'])
        date = donation['val']['Date Given']
        if len(date) > 11:
            date = date.split(' ')[0]
        date = date.split('/')
        if len(date[1]) == 1:
            date[1] = "0" + date[1]
        date = date[0] + '-' + date[1] + '-' + date[2]
        donation_dates.insert(0, date)
        donation_amounts.insert(0, float(donation['val']['Amount']))
        donation_types_graph[donation['val']['Source']] += float(donation['val']['Amount'])
    donation_dates, donation_amounts = zip(*sorted(zip(donation_dates, donation_amounts)))

    donation_dates_set = set(donation_dates)
    unique_dates = {}
    for date in donation_dates_set:
        if date not in unique_dates:
            unique_dates[date] = []
        unique_dates[date].append([index for index, value in enumerate(donation_dates) if value == date])

    donation_amounts_set = []
    donation_amounts = list(donation_amounts)
    for date in donation_dates_set:
        amount = 0
        for index in unique_dates[date]:
            for each in index:
                amount += float(donation_amounts[each])
        donation_amounts_set.append(amount)
    donation_dates_set = list(donation_dates_set)

    donation_dates_set, donation_amounts_set = zip(*sorted(zip(donation_dates_set, donation_amounts_set)))

    return donation_types_graph.keys(),donation_types_graph.values(), donation_dates_set, donation_amounts_set, donation_amount


def dataFrom(collection):
    data = [{'key': item.key(), 'val': item.val()} for item in DB.child(collection).get().each()]
    keys = [key.lower() for key in data[0]['val'].keys()]
    return data, keys

