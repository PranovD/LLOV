""" This module does blah blah blah """

import datetime
from flask import render_template, request
from flask_app import DB
from flask_app import APP
from flask_app import plaid_ctrl


@APP.route('/')
@APP.route('/index')
def index():
    """
    description
    """

    table = "donations"
    donation_data, donation_keys = DB.data_from(table)
    donation_amount = 0
    donation_dates = []
    donation_amounts = []
    donation_types_graph = {'Cash': 0, 'Check': 0, 'Venmo': 0, 'Cashapp': 0}

    for donation in donation_data:
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
    event_data, event_keys = db.DB.data_from(table)
    return render_template('main.html',
                           donation_pie_labels=donation_types_graph.keys(),
                           donation_pie_values=donation_types_graph.values(),
                           donation_dates=donation_dates,
                           donation_amounts=donation_amounts,
                           donation_graph_data=donation_data,
                           donation_amount=donation_amount,
                           event_data=event_data,
                           event_keys=event_keys,
                           page="Main")


@APP.route('/login')
def login():
    """
    description
    """
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
    return render_template('login.html')


@APP.route('/dog', methods=['POST'])
def post_dog():
    """
    description
    """
    new_foster_dog_data = {}
    # for field in form:
    #     new_foster_dog_data[field.name] = field.data

    db.DB.add_foster_dog(new_foster_dog_data)
    return render_template('dog.html', page="Foster Dog")


@APP.route('/volunteer', methods=['POST'])
def post_volunteer():
    """
    description
    """

    data = {
        'first_name': request.form.get('firstName'),
        'last_name': request.form.get('lastName'),
        'street': request.form.get('street'),
        'city': request.form.get('city'),
        'state': request.form.get('state'),
        'zipcode': request.form.get('zipcode'),
        'phone_number': request.form.get('number'),
        'volunteering': {
            'can_volunteer': request.form.get('volunteering'),
            'longterm': request.form.get('long-term-foster'),
            'shortterm': request.form.get('short-term-foster'),
            'emergency': request.form.get('emergency-foster'),
            'coord': request.form.get('coordinating'),
            'flyers': request.form.get('putting-up-flyers'),
            'dogwalking': request.form.get('dog-walking'),
            'fundraising': request.form.get('fundraisers'),
            'adoptions': request.form.get('helping-at-adoptions'),
            'transporting': request.form.get('transporting'),
            'vet': request.form.get('vet-appointments'),
            'other': request.form.get('volunteering-other')
        },
        'adoption_fostering': {
            'can_adopt': request.form.get('adopting'),
            'can_foster': request.form.get('fostering'),
            'dogTypes': {
                'female': request.form.get('female'),
                'male': request.form.get('male'),
                'small': request.form.get('small'),
                'large': request.form.get('large'),
                'breeds': request.form.get('breeds'),
                'other': request.form.get('fostering-other')
            }
        }
    }

    db.DB.add_volunteer(data)
    return render_template('volunteer.html', page="Volunteers")


@APP.route('/foster', methods=['POST'])
def post_to_fosters():
    """
    description
    """

    data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'street': request.form.get('street'),
        'city': request.form.get('city'),
        'state': request.form.get('state'),
        'zipcode': request.form.get('zipcode'),
        'can_adopt_more': request.form.get('can_adopt_more'),
        'comments': request.form.get('comments'),
        'timestamp': str(datetime.datetime.now())
    }
    db.DB.add_foster(data)
    return render_template('foster.html', page="Fosters")


@APP.route('/donation', methods=['POST'])
def post_to_donation():
    """
    description
    """

    data = {
        'first_name': request.form.get('firstName'),
        'last_name': request.form.get('lastName'),
        'amount': request.form.get('amount'),
        'comments': request.form.get('comments'),
        'source': request.form.get('source'),
        'timestamp': str(datetime.datetime.now())
    }
    db.DB.add_donation(data)
    return render_template('donation.html', page="Donations")


@APP.route('/data', methods=['POST', 'GET'])
def return_data():
    """
    description
    """

    get_data = None
    balance = None
    plaid_data = None
    get_keys = None
    table = request.args.get('table')

    if table is None:
        table = "donations"

    if table == "donations":
        plaid_data = plaid_ctrl.get_plaid_data(request.args.get('request'))

    get_data, get_keys = db.DB.data_from(table)
    return render_template('data.html', data=get_data, get_keys=get_keys,
                           page=table, balance=balance, plaid_data=plaid_data)


@APP.route('/update', methods=['POST', 'GET'])
def update():
    """
    description
    """
    print(request.args)
    return return_data()


@APP.route('/on_app_load')
def on_app_load():
    """
    description
    """
    pass
