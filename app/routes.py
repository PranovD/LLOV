""" This module does blah blah blah """

import datetime
from flask import render_template, request
from app import app, db


@app.route('/')
def index():
    """
    description
    """

    table = "donations"
    donation_data, donation_keys = db.data_from(table)
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
    event_data, event_keys = db.data_from(table)
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


@app.route('/login')
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


@app.route('/dog', methods=['POST', 'GET'])
def post_to_dog():
    """
    description
    """

    error_data = None
    new_foster_dog_data = {}

    if request.method == 'POST':
        for field in form:
            if db.sanitize_user_input(field.data) is None or \
                    db.sanitize_user_input(field.name) is None:
                error_data = "All fields must be filled out"
            else:
                new_foster_dog_data[db.sanitize_user_input(field.name)] \
                    = db.sanitize_user_input(field.data)

    if error_data is None:
        db.add_foster_dog(new_foster_dog_data)

    return render_template('dog.html', page="Foster Dog",
                           error_data=error_data)


@app.route('/volunteer', methods=['POST', 'GET'])
def volunteers():
    """
    description
    """

    error_data = ""

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        # email = request.form.get('email')
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
        shortterm = request.form.get('short-term-foster')
        emergency = request.form.get('emergency-foster')
        coord = request.form.get('coordinating')
        flyers = request.form.get('putting-up-flyers')
        dogwalking = request.form.get('dog-walking')
        fundraising = request.form.get('fundraisers')
        adoptions = request.form.get('helping-at-adoptions')
        transporting = request.form.get('transporting')
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

        DB.child("volunteers").push(data)

    return render_template('volunteer.html', page="Volunteers",
                           error=error, error_data=error_data)


@app.route('/foster', methods=['POST', 'GET'])
def post_to_fosters():
    """
    description
    """

    error = False
    error_data = ""

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        # phone = request.form.get('number')
        can_adopt_more = request.form.get('source')
        comments = request.form.get('comments')

        if first_name is None or not first_name or last_name is None \
                or not last_name:
            error = True
            error_data = "All fields must be filled out."

        if not error:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'street': street,
                'city': city,
                'state': state,
                'zipcode': zipcode,
                'can_adopt_more': can_adopt_more,
                'comments': comments,
                'timestamp': str(datetime.datetime.now())
            }
            DB.child("fosters").push(data)

    return render_template('foster.html', page="Fosters", error=error,
                           error_data=error_data)


@app.route('/donation', methods=['POST', 'GET'])
def postToDonation():
    """
    description
    """

    error = False
    error_data = ""

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        amount = request.form.get('amount')
        source = request.form.get('source')
        comments = request.form.get('comments')

        if first_name is None or last_name is None or source is None \
                or not first_name or not source \
                or not last_name:
            error = True
            error_data = "All fields must be filled out."

        if not error:
            try:
                amount = float(amount)

                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'amount': amount,
                    'comments': comments,
                    'source': source,
                    'timestamp': str(datetime.datetime.now())
                }

                DB.child("donations").push(data)

            except:
                error = True
                error_data = "Amount field has to be a valid $ amount."

    return render_template('donation.html', page="Donations",
                           error=error, error_data=error_data)


@app.route('/get_plaid_data', methods=['POST'])
def get_plaid_data(plaid_request, error_data):
    try:
        balance_response = CLIENT.Accounts.balance.get(ACCESS_TOKEN)
        balance = json.dumps(balance_response, indent=2,
                             sort_keys=True)

    except plaid.errors.PlaidError as err:
        error_data = jsonify({'error': {'display_message':
                                        err.display_message,
                                        'error_code': err.code,
                                            'error_type': err.type}})
        raise InvalidUsage('This view is gone', status_code=410)

@app.route('/data', methods=['POST', 'GET'])
def return_data():
    """
    description
    """

    get_data = None
    balance = None
    plaid_data = None
    error_data = None
    get_keys = None
    table = request.args.get('table')

    if table is None:
        table = "donations"

    if table == "donations":
        plaid_data = get_plaid_data(request.args.get('request'), error_data)

    get_data, get_keys = db.data_from(table)
    return render_template('data.html', data=get_data, get_keys=get_keys,
                           page=table, error_data=error_data, balance=balance,
                           plaid_data=plaid_data)

@app.route('/update', methods=['POST', 'GET'])
def update():
    """
    description
    """

    print(request.args)
    return return_data()


@app.route('/on_app_load')
def on_app_load():
    """
    description
    """

    pass


