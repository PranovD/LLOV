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
    donation_pie_labels, donation_pie_values, donation_dates, donation_amounts, donation_amount  = donations_graph_data()

    return render_template('dashboard.html', page="Dash",
                           event_data=event_data,
                           donation_data=donation_data,
                           donation_pie_labels=donation_pie_labels,
                           donation_pie_values=donation_pie_values,
                           donation_dates=donation_dates,
                           donation_amounts=donation_amounts,
                           donation_amount=donation_amount,
                           plaid_public_key=PLAID_API_KEYS["plaid_public_key"])


@APP.route('/login')
def login():
    """
    description

    Going to move the notes below into separate authorization controller - MA
    """
    """
    Act management actions like changing pwd should be in separate route - MA

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



def donations_graph_data():
    table = "donations"
    donnation_data, donnation_keys = dataFrom(table)
    donation_amount = 0
    donation_dates = []
    donation_amounts = []
    donation_types_graph = {'Cash': 0, 'Check': 0, 'Venmo': 0, 'Cashapp': 0, 'Bank Transaction': 0}
    for donation in donnation_data:
        donation_amount += float(donation['val']['Amount'])
        date = donation['val']['Date Given']
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
    data = [{'key': item.key(), 'val': item.val()} for item in db.DB.child(collection).get().each()]
    keys = [key.lower() for key in data[0]['val'].keys()]
    return data, keys