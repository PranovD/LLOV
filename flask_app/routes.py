"""
If adding a new route, make sure it belongs here and wouldn't make more sense
    in a controller. If you're making a call to Plaid or FB, a new route
    probably belongs in one of the controllers
    (not applicable if just renaming routes) - MA
"""

from flask import render_template, request
from flask_app import APP
from flask_app import plaid_ctrl, db, errors
# from forms_ctrl import WHITELISTED_FORMS


@APP.route('/')
@APP.route('/dashboard')
def dashboard():
    """
    description
    """
    event_data = db.get_firebase_collection("events")
    donation_data = db.get_firebase_collection("donations")

    return render_template('dashboard.html', page="Dash",
                           event_data=event_data,
                           donation_data=donation_data)


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
def post_new_form():
    """
    description
    """
    return render_template('create_new_form.html')


@APP.route('/forms/<form>', methods=['GET', 'POST'])
def display_form(form):
    """
    description
    """
    clean_form = db.sanitize_user_input(form)

    form_object = forms_ctrl.create_form_object(clean_form)
    html_form_type = forms_ctrl.get_html_form_type(clean_form)
    # if form_object.validate_on_submit():

    return render_template('form_base.html', page=clean_form,
                           form=form_object,
                           specific_form_html=html_form_type)


# @APP.route('/forms/<form>', methods=['GET', 'POST'])
# def display_form(form):
#     """
#     description
#     """
#     if form not in white_listed_forms:
#         raise errors.InvalidUsage("We are currently not storing \
#                                   this data.", status_code=410)
#     else:
#         if request.method == 'POST':
#             new_data = {}
#             # WTForms needed for this: - MA
#             # for field in form:
#             #     new_foster_dog_data[field.name] = field.data
#
#             db.add_firebase_document(form, new_data)
#
#     return render_template('<form>_form.html', page="<form>")


@APP.route('/forms/volunteer', methods=['GET', 'POST'])
def volunteer_form():
    """
    description
    """

    if request.method == 'POST':
        new_volunteer_data = {}
        # I want to convert listing the data manually like below
        # to list data automatically like in this for loop: -MA
        # Need to implement WTForms for this - MA
        # for field in form:
        #     new_volunteer_data[field.name] = field.data

        # data = {
        #     'first_name': request.form.get('firstName'),
        #     'last_name': request.form.get('lastName'),
        #     'street': request.form.get('street'),
        #     'city': request.form.get('city'),
        #     'state': request.form.get('state'),
        #     'zipcode': request.form.get('zipcode'),
        #     'phone_number': request.form.get('number'),
        #     'volunteering': {
        #         'can_volunteer': request.form.get('volunteering'),
        #         'longterm': request.form.get('long-term-foster'),
        #         'shortterm': request.form.get('short-term-foster'),
        #         'emergency': request.form.get('emergency-foster'),
        #         'coord': request.form.get('coordinating'),
        #         'flyers': request.form.get('putting-up-flyers'),
        #         'dogwalking': request.form.get('dog-walking'),
        #         'fundraising': request.form.get('fundraisers'),
        #         'adoptions': request.form.get('helping-at-adoptions'),
        #         'transporting': request.form.get('transporting'),
        #         'vet': request.form.get('vet-appointments'),
        #         'other': request.form.get('volunteering-other')
        #     },
        #     'adoption_fostering': {
        #         'can_adopt': request.form.get('adopting'),
        #         'can_foster': request.form.get('fostering'),
        #         'dogTypes': {
        #             'female': request.form.get('female'),
        #             'male': request.form.get('male'),
        #             'small': request.form.get('small'),
        #             'large': request.form.get('large'),
        #             'breeds': request.form.get('breeds'),
        #             'other': request.form.get('fostering-other')
        #         }
        #     }
        # }

        db.add_firebase_document("volunteers", new_volunteer_data)
    return render_template('volunteer_intake_form.html', page="Volunteers")


@APP.route('/forms/foster', methods=['GET', 'POST'])
def foster_form():
    """
    description
    """

    if request.method == 'POST':
        new_foster_data = {}
        # I want to convert listing the data manually like below
        # to list data automatically like in this for loop: - MA
        # Need to implement WTForms for this - MA
        # for field in form:
        #     new_foster_data[field.name] = field.data

        # data = {
        #     'first_name': request.form.get('first_name'),
        #     'last_name': request.form.get('last_name'),
        #     'street': request.form.get('street'),
        #     'city': request.form.get('city'),
        #     'state': request.form.get('state'),
        #     'zipcode': request.form.get('zipcode'),
        #     'can_adopt_more': request.form.get('can_adopt_more'),
        #     'comments': request.form.get('comments'),
        #     'timestamp': str(datetime.datetime.now())
        # }

        db.add_firebase_document("fosters", new_foster_data)
    return render_template('foster_volunteer_intake_form.html', page="Fosters")


@APP.route('/forms/donation', methods=['GET', 'POST'])
def donation_form():
    """
    description
    """

    if request.method == 'POST':
        new_donation_data = {}
        # I want to convert listing the data manually like below
        # to list data automatically like in this for loop: - MA
        # Need to implement WTForms for this - MA
        # for field in form:
        #     new_donation_data[field.name] = field.data

        # data = {
        #     'first_name': request.form.get('firstName'),
        #     'last_name': request.form.get('lastName'),
        #     'amount': request.form.get('amount'),
        #     'comments': request.form.get('comments'),
        #     'source': request.form.get('source'),
        #     'timestamp': str(datetime.datetime.now())
        # }
        db.add_firebase_document("donations", new_donation_data)
    return render_template('new_donation_form.html', page="Donations")


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


@APP.route('/update', methods=['POST', 'GET'])
def update():
    """
    description

    Same as above method, needs more description. Whats being updated? - MA
    """
    collection = db.sanitize_user_input(request.args.get('table'))
    return db.get_firebase_collection(collection)


@APP.route('/on_app_load')
def on_app_load():
    """
    description

    See above ^  - MA
    """
    pass
